"""
Evaluation Harness for The Edge Grid Verification Track.

Orchestrates:
1. Loading TruthfulQA subset.
2. Generating honest edge-node answers (via Ollama or simulated via Groq fast model).
3. Injecting fraud across 4 corruption strategies.
4. Scoring all answers with the LLM-as-Judge (1-5 scale + PASS/FAIL).
5. Computing precision, recall, F1, and score distribution metrics.
6. Exporting raw and summary CSV tables to docs/results/ for the paper.
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root and verification folder are on sys.path
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import (
    GROQ_API_KEY,
    GROQ_JUDGE_MODEL,
    GROQ_SIMULATOR_MODEL,
    OLLAMA_URL,
    OLLAMA_MODEL,
    RESULTS_DIR,
    TRUTHFULQA_SUBSET_SIZE,
)
from evaluator import Judge, append_result
from truthfulqa_loader import load_truthfulqa_subset
from fraud_injector import inject_fraud

try:
    from groq import Groq
except ImportError:
    Groq = None
import requests


def generate_honest_answer(
    question: str,
    reference_answer: str = "",
    use_ollama: bool = False,
    groq_client: Any = None,
    simulator_model: str = GROQ_SIMULATOR_MODEL,
) -> str:
    """Generates an honest answer simulating an edge worker node."""
    system_prompt = "You are a helpful, accurate AI assistant. Answer the user's question directly, truthfully, and concisely in 1-2 sentences."
    
    if use_ollama:
        try:
            resp = requests.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": f"{system_prompt}\n\nQuestion: {question}",
                    "stream": False,
                },
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            print(f"Ollama generation failed ({e}), falling back to Groq simulator...")

    # Groq simulator fallback
    if groq_client:
        completion = groq_client.chat.completions.create(
            model=simulator_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=150,
            timeout=30.0,
        )
        return completion.choices[0].message.content.strip()

    return reference_answer or "No generation backend available."


def run_evaluation(
    subset_size: int = 10,
    strategies: List[str] = None,
    use_ollama: bool = False,
    judge_backend: str = "groq",
    judge_model: str = GROQ_JUDGE_MODEL,
    delay: float = 1.5,
):
    if strategies is None:
        strategies = ["swap_incorrect", "negate", "hallucinate_entity", "random_topic"]

    print("=" * 70)
    print("THE EDGE GRID - AGENTIC VERIFICATION & EVALUATION HARNESS")
    print(f"Subset size: {subset_size} questions")
    print(f"Strategies : {', '.join(strategies)}")
    print(f"Judge      : {judge_backend} ({judge_model})")
    print(f"Generator  : {'Ollama (' + OLLAMA_MODEL + ')' if use_ollama else 'Groq Simulator (' + GROQ_SIMULATOR_MODEL + ')'}")
    print("=" * 70)

    # Initialize components
    judge = Judge(backend=judge_backend, model=judge_model)
    groq_client = Groq(api_key=GROQ_API_KEY) if (GROQ_API_KEY and Groq) else None

    # Load dataset
    questions = load_truthfulqa_subset(n=subset_size)
    all_best_answers = [q["best_answer"] for q in questions]

    raw_results_file = os.path.join(RESULTS_DIR, "verification_results.csv")
    summary_file = os.path.join(RESULTS_DIR, "verification_summary.csv")

    # Clear previous results for fresh run
    if os.path.exists(raw_results_file):
        os.remove(raw_results_file)

    evaluated_records = []
    total_evals = len(questions) * (1 + len(strategies))
    current_eval = 0

    print(f"\nRunning {total_evals} total evaluations with {delay}s delay...")

    for q_item in questions:
        q_id = q_item["question_id"]
        q_text = q_item["question"]
        best_ans = q_item["best_answer"]
        incorrect_list = q_item["incorrect_answers"]

        # 1. Honest condition
        current_eval += 1
        print(f"[{current_eval}/{total_evals}] Q{q_id} Honest Answer...", end=" ", flush=True)
        honest_answer = generate_honest_answer(
            question=q_text,
            reference_answer=best_ans,
            use_ollama=use_ollama,
            groq_client=groq_client,
        )
        time.sleep(delay)

        honest_eval = judge.score(prompt=q_text, output=honest_answer)
        time.sleep(delay)

        honest_record = {
            "question_id": q_id,
            "question": q_text,
            "answer": honest_answer,
            "is_fraud": False,
            "fraud_strategy": "none (honest)",
            "score": honest_eval["score"],
            "verdict": honest_eval["verdict"],
            "expected_verdict": "pass",
            "correct_classification": honest_eval["verdict"] == "pass",
            "reason": honest_eval["reason"],
            "judge_model": judge_model,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        append_result(raw_results_file, honest_record)
        evaluated_records.append(honest_record)
        print(f"Score: {honest_eval['score']}/5 [{honest_eval['verdict'].upper()}]")

        # 2. Fraud conditions
        for strat in strategies:
            current_eval += 1
            print(f"[{current_eval}/{total_evals}] Q{q_id} Fraud ({strat})...", end=" ", flush=True)
            corrupted_ans, strat_used = inject_fraud(
                question=q_text,
                correct_answer=best_ans,
                incorrect_answers=incorrect_list,
                strategy=strat,
                all_answers_pool=all_best_answers,
                seed=q_id,
            )

            fraud_eval = judge.score(prompt=q_text, output=corrupted_ans)
            time.sleep(delay)

            fraud_record = {
                "question_id": q_id,
                "question": q_text,
                "answer": corrupted_ans,
                "is_fraud": True,
                "fraud_strategy": strat_used,
                "score": fraud_eval["score"],
                "verdict": fraud_eval["verdict"],
                "expected_verdict": "fail",
                "correct_classification": fraud_eval["verdict"] == "fail",
                "reason": fraud_eval["reason"],
                "judge_model": judge_model,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            append_result(raw_results_file, fraud_record)
            evaluated_records.append(fraud_record)
            print(f"Score: {fraud_eval['score']}/5 [{fraud_eval['verdict'].upper()}]")

    # 3. Compute Metrics
    print("\n" + "=" * 70)
    print("COMPUTING SUMMARY METRICS FOR RESEARCH PAPER")
    print("=" * 70)

    summary_rows = []
    
    # Calculate for each strategy and overall
    all_categories = list(set(r["fraud_strategy"] for r in evaluated_records if r["is_fraud"]))
    
    def calculate_metrics_for_subset(records_subset, cat_name):
        # In fraud detection:
        # Positive = Fraud (is_fraud=True)
        # Negative = Honest (is_fraud=False)
        # TP = is_fraud=True and verdict=="fail" (Fraud correctly flagged)
        # FN = is_fraud=True and verdict=="pass" (Fraud missed)
        # TN = is_fraud=False and verdict=="pass" (Honest correctly passed)
        # FP = is_fraud=False and verdict=="fail" (Honest falsely rejected)
        
        fraud_items = [r for r in records_subset if r["is_fraud"]]
        honest_items = [r for r in evaluated_records if not r["is_fraud"]]

        tp = sum(1 for r in fraud_items if r["verdict"] == "fail")
        fn = sum(1 for r in fraud_items if r["verdict"] == "pass")
        tn = sum(1 for r in honest_items if r["verdict"] == "pass")
        fp = sum(1 for r in honest_items if r["verdict"] == "fail")

        n_total = len(fraud_items) + len(honest_items)
        precision = (tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        recall = (tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        accuracy = ((tp + tn) / n_total) if n_total > 0 else 0.0

        mean_fraud_score = sum(r["score"] for r in fraud_items) / len(fraud_items) if fraud_items else 0.0
        mean_honest_score = sum(r["score"] for r in honest_items) / len(honest_items) if honest_items else 0.0

        return {
            "strategy": cat_name,
            "TP": tp,
            "FP": fp,
            "TN": tn,
            "FN": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "accuracy": round(accuracy, 4),
            "mean_score_honest": round(mean_honest_score, 2),
            "mean_score_fraud": round(mean_fraud_score, 2),
            "N_fraud": len(fraud_items),
            "N_honest": len(honest_items),
        }

    for cat in sorted(all_categories):
        subset = [r for r in evaluated_records if r["fraud_strategy"] == cat]
        summary_rows.append(calculate_metrics_for_subset(subset, cat))

    overall_row = calculate_metrics_for_subset(evaluated_records, "OVERALL")
    summary_rows.append(overall_row)

    # Save summary CSV
    if os.path.exists(summary_file):
        os.remove(summary_file)
    for row in summary_rows:
        append_result(summary_file, row)

    # Display clean table to stdout
    header_fmt = "{:<25} | {:<5} | {:<5} | {:<5} | {:<5} | {:<9} | {:<8} | {:<6} | {:<8} | {:<8}"
    print(header_fmt.format("Strategy", "TP", "FP", "TN", "FN", "Precision", "Recall", "F1", "Honest µ", "Fraud µ"))
    print("-" * 105)
    for row in summary_rows:
        print(header_fmt.format(
            row["strategy"],
            row["TP"], row["FP"], row["TN"], row["FN"],
            f"{row['precision']:.2%}",
            f"{row['recall']:.2%}",
            f"{row['f1']:.3f}",
            f"{row['mean_score_honest']}/5",
            f"{row['mean_score_fraud']}/5",
        ))
    print("-" * 105)
    print(f"\nRaw results saved to    : {raw_results_file}")
    print(f"Summary metrics saved to: {summary_file}")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Edge Grid Verification & Evaluation Harness")
    parser.add_argument("--subset-size", type=int, default=TRUTHFULQA_SUBSET_SIZE, help="Number of TruthfulQA questions")
    parser.add_argument("--strategies", type=str, default="swap_incorrect,negate,hallucinate_entity,random_topic", help="Comma-separated fraud strategies")
    parser.add_argument("--use-ollama", action="store_true", help="Use local Ollama for inference generation")
    parser.add_argument("--judge-backend", type=str, default="groq", choices=["groq", "ollama"], help="Judge backend")
    parser.add_argument("--judge-model", type=str, default=GROQ_JUDGE_MODEL, help="Judge model name")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay in seconds between calls")

    args = parser.parse_args()
    strats = [s.strip() for s in args.strategies.split(",") if s.strip()]

    run_evaluation(
        subset_size=args.subset_size,
        strategies=strats,
        use_ollama=args.use_ollama,
        judge_backend=args.judge_backend,
        judge_model=args.judge_model,
        delay=args.delay,
    )
