"""
End-to-End Integration Runner for The Edge Grid.

Chains:
Track B (Inference Engine) -> Track C (LLM-as-Judge Verifier) -> Track D (Simulated Ledger Settlement)

Demonstrates:
1. Provider registers stake on ledger.
2. Inference executed on edge node.
3. Judge scores result (quality score 1-5, PASS/FAIL).
4. Ledger settles payment or slashes stake upon failure.
5. Exports complete transaction history to CSV.
"""

import os
import sys
import uuid
from pathlib import Path

# Ensure paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from verification.config import RESULTS_DIR, GROQ_API_KEY
from verification.evaluator import Judge, append_result
from contracts.simulate import SimulatedLedger, centralized_cost


def run_pipeline_demo():
    print("=" * 70)
    print("THE EDGE GRID - FULL PIPELINE INTEGRATION RUNNER")
    print("Inference -> Verification -> Settlement")
    print("=" * 70)

    # 1. Initialize Track D Ledger
    ledger = SimulatedLedger()
    peers = ["node-alpha-1", "node-beta-2", "node-gamma-3"]
    initial_stake = 10.0
    for p in peers:
        ledger.register_stake(p, initial_stake)
    print(f"\n[1] Initialized Ledger: Registered peers {peers} with {initial_stake} ETH stake each.")

    # 2. Initialize Track C Judge
    judge = Judge(backend="groq")
    print(f"[2] Initialized Judge: {judge.model} via Groq.")

    # 3. Setup test jobs (mix of honest prompts, hallucinated outputs, and edge cases)
    test_jobs = [
        {
            "job_id": str(uuid.uuid4())[:8],
            "peer": "node-alpha-1",
            "prompt": "What causes tides on Earth?",
            "output": "Ocean tides are caused by gravitational forces exerted by the Moon and the Sun upon the Earth's oceans.",
            "price": 0.25,
        },
        {
            "job_id": str(uuid.uuid4())[:8],
            "peer": "node-beta-2",
            "prompt": "What is the primary gas in Earth's atmosphere?",
            "output": "Nitrogen makes up approximately 78% of Earth's atmosphere by volume.",
            "price": 0.20,
        },
        {
            "job_id": str(uuid.uuid4())[:8],
            "peer": "node-alpha-1",
            "prompt": "Can humans breathe underwater without equipment?",
            "output": "Yes, with proper meditation and lung training, humans can absorb oxygen directly from water.",
            "price": 0.30,  # Blatant hallucination -> should be slashed
        },
        {
            "job_id": str(uuid.uuid4())[:8],
            "peer": "node-gamma-3",
            "prompt": "What is the boiling point of water at sea level?",
            "output": "Water boils at 100 degrees Celsius (212 degrees Fahrenheit) at standard atmospheric pressure.",
            "price": 0.15,
        },
    ]

    integration_log_file = os.path.join(RESULTS_DIR, "integration_results.csv")
    if os.path.exists(integration_log_file):
        os.remove(integration_log_file)

    print(f"\n[3] Processing {len(test_jobs)} inference jobs through Judge and Settlement Ledger:\n")

    for idx, job in enumerate(test_jobs, 1):
        print(f"--- Job {idx} (ID: {job['job_id']}) by {job['peer']} ---")
        print(f"Prompt : {job['prompt']}")
        print(f"Output : {job['output']}")

        # Track C: Judge Verification
        inference_result = {
            "job_id": job["job_id"],
            "output": job["output"],
            "tokens_generated": len(job["output"].split()),
            "latency_ms": 120.0,
            "output_hash": "sha256_mock_hash",
        }
        verdict_data = judge.score_inference_result(prompt=job["prompt"], inference_result=inference_result)
        
        verdict = verdict_data["verdict"]
        score = verdict_data.get("quality_score", 3)
        reason = verdict_data["reason"]
        print(f"Judge  : Quality Score {score}/5 -> Verdict [{verdict.upper()}] (Reason: {reason})")

        # Track D: Settlement
        settlement_rec = ledger.settle(
            job_id=job["job_id"],
            provider_peer_id=job["peer"],
            amount=job["price"],
            verdict=verdict,
        )

        status_str = f"SLASHED (-{settlement_rec['slash_amount']} ETH)" if settlement_rec["slashed"] else f"PAID (+{settlement_rec['amount']} ETH)"
        print(f"Ledger : {status_str} | Remaining stake: {ledger.stakes[job['peer']]:.2f} ETH\n")

        # Log combined pipeline record
        log_row = {
            "job_id": job["job_id"],
            "provider_peer_id": job["peer"],
            "prompt": job["prompt"],
            "output": job["output"],
            "judge_quality_score": score,
            "judge_verdict": verdict,
            "judge_reason": reason,
            "amount": job["price"],
            "slashed": settlement_rec["slashed"],
            "slash_amount": settlement_rec["slash_amount"],
            "remaining_stake": ledger.stakes[job["peer"]],
        }
        append_result(integration_log_file, log_row)

    print("=" * 70)
    print("FINAL INTEGRATION SUMMARY")
    print("=" * 70)
    print(f"Remaining node stakes: {ledger.stakes}")
    print(f"Total settled payout : {ledger.total_cost():.4f} ETH")
    
    comp_cost = centralized_cost(num_jobs=len(test_jobs), tokens_per_job=30, price_per_1k_tokens=0.002)
    print(f"Centralized baseline : ${comp_cost:.6f}")
    print(f"Pipeline logs saved  : {integration_log_file}")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline_demo()
