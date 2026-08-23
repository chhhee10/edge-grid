"""
LLM-as-judge validator + evaluation harness.

Scores an inference_result (see ../shared/schemas.md) as pass/fail, and aggregates
metrics for the experiments in ../docs/EXPERIMENTS.md.
"""

import csv
import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
JUDGE_PROMPT_TEMPLATE = """You are grading an AI-generated answer for factual correctness.

Question: {prompt}
Answer: {output}

Is this answer factually correct and non-hallucinated? Respond with exactly one word: PASS or FAIL."""


class Judge:
    def __init__(self, model: str = "qwen2.5:1.5b"):
        self.model = model

    def score(self, prompt: str, output: str) -> dict:
        judge_prompt = JUDGE_PROMPT_TEMPLATE.format(prompt=prompt, output=output)
        response = requests.post(
            OLLAMA_URL,
            json={"model": self.model, "prompt": judge_prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        verdict_text = response.json()["response"].strip().upper()
        verdict = "pass" if "PASS" in verdict_text else "fail"
        return {"verdict": verdict, "judge_score": 1.0 if verdict == "pass" else 0.0, "reason": verdict_text}


def append_result(csv_path: str, row: dict):
    file_exists = os.path.exists(csv_path)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def load_truthfulqa_subset(path: str = "data/truthfulqa_subset.csv") -> list[dict]:
    # TODO: point at the subset pulled from the lit survey
    raise NotImplementedError


if __name__ == "__main__":
    judge = Judge()
    print(judge.score(prompt="What causes tides?", output="Tides are caused by lunar gravity."))
