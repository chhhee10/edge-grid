"""
LLM-as-judge validator + evaluation harness for The Edge Grid.

Scores AI-generated answers for factual correctness on a 1-5 quality scale
and assigns a PASS/FAIL verdict. Supports Groq (default, Llama 3 70B) and Ollama backends.
"""

import csv
import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any

try:
    from groq import Groq
except ImportError:
    Groq = None

import requests

try:
    from .config import (
        GROQ_API_KEY,
        GROQ_JUDGE_MODEL,
        OLLAMA_URL,
        OLLAMA_MODEL,
        PASS_THRESHOLD,
    )
except (ImportError, ValueError):
    from config import (
        GROQ_API_KEY,
        GROQ_JUDGE_MODEL,
        OLLAMA_URL,
        OLLAMA_MODEL,
        PASS_THRESHOLD,
    )

JUDGE_SYSTEM_PROMPT = """You are an expert fact-checker grading AI-generated answers for factual accuracy.

Scoring Rubric:
5 = Completely correct, accurate, and directly answers the question with no falsehoods.
4 = Mostly correct with minor omissions or slight imprecision, but fundamentally truthful.
3 = Partially correct, but contains notable inaccuracies, ambiguities, or misleading framing.
2 = Mostly incorrect, contains clear factual errors or hallucinations.
1 = Completely wrong, fabricated, nonsensical, or entirely off-topic.

Decision Rules:
- Score 3, 4, or 5 -> verdict is "PASS"
- Score 1 or 2 -> verdict is "FAIL"

You MUST respond ONLY with a valid JSON object in this exact format:
{
  "score": <integer from 1 to 5>,
  "verdict": "<PASS or FAIL>",
  "reason": "<one or two sentences explaining your evaluation>"
}"""

JUDGE_USER_PROMPT = """Question: {prompt}
AI-Generated Answer: {output}

Evaluate the answer now."""


class Judge:
    def __init__(
        self,
        backend: str = "groq",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        pass_threshold: int = PASS_THRESHOLD,
    ):
        self.backend = backend.lower()
        self.pass_threshold = pass_threshold
        self.api_key = api_key or GROQ_API_KEY

        if self.backend in ["groq", "auto"]:
            self.model = model or GROQ_JUDGE_MODEL
            if Groq is None:
                raise ImportError("The 'groq' package is not installed. Please run pip install groq")
            if not self.api_key:
                print("Notice: GROQ_API_KEY is not set. Falling back to local heuristic/mock judge mode.")
                self.backend = "mock"
                self.client = None
            else:
                self.client = Groq(api_key=self.api_key)
        elif self.backend == "ollama":
            self.model = model or OLLAMA_MODEL
            self.client = None
        elif self.backend in ["mock", "simulated"]:
            self.model = "heuristic-rule-judge"
            self.client = None
        else:
            raise ValueError(f"Unsupported backend: {backend}. Use 'groq', 'ollama', or 'mock'.")

    def _parse_judge_response(self, text: str) -> Dict[str, Any]:
        """Robustly extract score, verdict, and reason from model output."""
        text = text.strip()
        # Try direct JSON parsing
        try:
            data = json.loads(text)
            score = int(data.get("score", 1))
            score = max(1, min(5, score))
            verdict = str(data.get("verdict", "")).strip().lower()
            if verdict not in ["pass", "fail"]:
                verdict = "pass" if score >= self.pass_threshold else "fail"
            reason = str(data.get("reason", "")).strip()
            return {"score": score, "verdict": verdict, "reason": reason}
        except Exception:
            pass

        # Fallback: extract json block using regex
        json_match = re.search(r"\{.*?\}", text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                score = int(data.get("score", 1))
                score = max(1, min(5, score))
                verdict = str(data.get("verdict", "")).strip().lower()
                if verdict not in ["pass", "fail"]:
                    verdict = "pass" if score >= self.pass_threshold else "fail"
                reason = str(data.get("reason", "")).strip()
                return {"score": score, "verdict": verdict, "reason": reason}
            except Exception:
                pass

        # Fallback: heuristic regex search for score and verdict
        score_match = re.search(r"score[\"':\s]+([1-5])", text, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 3

        if "PASS" in text.upper() and "FAIL" not in text.upper():
            verdict = "pass"
        elif "FAIL" in text.upper() and "PASS" not in text.upper():
            verdict = "fail"
        else:
            verdict = "pass" if score >= self.pass_threshold else "fail"

        return {
            "score": score,
            "verdict": verdict,
            "reason": text[:200].replace("\n", " "),
        }

    def score(self, prompt: str, output: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        Scores an AI answer for factual correctness.
        Returns:
            dict with {score, verdict, judge_score, reason, model, backend, timestamp}
        """
        for attempt in range(max_retries + 1):
            try:
                if self.backend == "groq":
                    if not self.client:
                        if not self.api_key:
                            raise ValueError(
                                "GROQ_API_KEY is not set. Please add it to verification/.env or environment variables."
                            )
                        self.client = Groq(api_key=self.api_key)

                    completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                            {"role": "user", "content": JUDGE_USER_PROMPT.format(prompt=prompt, output=output)},
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.1,
                        max_tokens=256,
                        timeout=30.0,
                    )
                    raw_text = completion.choices[0].message.content or "{}"
                elif self.backend in ["mock", "simulated"]:
                    # Heuristic evaluation for testing without active API credentials
                    p_lower = prompt.lower()
                    o_lower = output.lower()
                    
                    # Check for explicit negation or obvious falsehood markers
                    neg_markers = ["not caused by", "never", "cannot absorb", "10%", "blue before", "earthquakes", "photosynthesis", "treaty of versailles"]
                    has_neg = any(m in o_lower for m in neg_markers)
                    
                    # Check overlap with key words
                    p_words = set(re.findall(r"\w+", p_lower)) - {"what", "is", "the", "are", "causes", "in", "on", "of", "to", "a", "an"}
                    overlap = sum(1 for w in p_words if w in o_lower)
                    
                    if has_neg or overlap == 0:
                        raw_text = json.dumps({
                            "score": 1,
                            "verdict": "FAIL",
                            "reason": "Answer contains factual negations, falsehood markers, or is off-topic."
                        })
                    else:
                        raw_text = json.dumps({
                            "score": 5,
                            "verdict": "PASS",
                            "reason": "Answer is factually consistent and addresses the prompt."
                        })
                else:
                    # Ollama backend
                    full_prompt = f"{JUDGE_SYSTEM_PROMPT}\n\n{JUDGE_USER_PROMPT.format(prompt=prompt, output=output)}"
                    resp = requests.post(
                        OLLAMA_URL,
                        json={"model": self.model, "prompt": full_prompt, "stream": False, "format": "json"},
                        timeout=60,
                    )
                    resp.raise_for_status()
                    raw_text = resp.json().get("response", "{}")

                parsed = self._parse_judge_response(raw_text)
                return {
                    "score": parsed["score"],
                    "verdict": parsed["verdict"],
                    "judge_score": float(parsed["score"]),
                    "reason": parsed["reason"],
                    "model": self.model,
                    "backend": self.backend,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            except Exception as e:
                if attempt == max_retries:
                    # Return safe failure verdict on complete breakdown
                    return {
                        "score": 1,
                        "verdict": "fail",
                        "judge_score": 1.0,
                        "reason": f"Evaluation error: {str(e)}",
                        "model": self.model,
                        "backend": self.backend,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                time.sleep(1.0)

    def score_inference_result(self, prompt: str, inference_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts an inference_result schema from Track B and produces a validation_verdict schema.
        See shared/schemas.md.
        """
        job_id = inference_result.get("job_id", "")
        output = inference_result.get("output", "")
        evaluation = self.score(prompt=prompt, output=output)

        return {
            "job_id": job_id,
            "verdict": evaluation["verdict"],
            "judge_score": evaluation["judge_score"],
            "reason": evaluation["reason"],
            "quality_score": evaluation["score"],
        }


def append_result(csv_path: str, row: dict):
    """Appends a result dictionary to a CSV file, creating directories and header if needed."""
    file_exists = os.path.exists(csv_path)
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    judge = Judge()
    test_res = judge.score(
        prompt="What causes ocean tides on Earth?",
        output="Ocean tides are caused primarily by the gravitational pull of the Moon and the Sun on Earth's oceans.",
    )
    print("Test scoring output:")
    print(json.dumps(test_res, indent=2))
