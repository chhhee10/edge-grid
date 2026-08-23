"""
Local settlement simulation — the actual settlement logic used in the demo.

Mirrors the staking/escrow/slashing rules sketched in contracts/*.sol, without
requiring deployment. See ../shared/schemas.md for the settlement_record shape.
"""

import csv
import os


class DuplicateSettlementError(Exception):
    """Raised when a job_id is settled more than once."""


class SimulatedLedger:
    def __init__(self):
        self.stakes: dict[str, float] = {}
        self.records: list[dict] = []
        self._settled_job_ids: set[str] = set()

    def register_stake(self, peer_id: str, amount: float):
        self.stakes[peer_id] = self.stakes.get(peer_id, 0.0) + amount

    def settle(self, job_id: str, provider_peer_id: str, amount: float, verdict: str) -> dict:
        if job_id in self._settled_job_ids:
            raise DuplicateSettlementError(f"job {job_id} already settled")

        slashed = verdict == "fail"
        available_stake = self.stakes.get(provider_peer_id, 0.0)
        if slashed:
            # Slash whatever stake remains, even if it's less than `amount` (insufficient stake).
            slash_amount = min(amount, available_stake)
            self.stakes[provider_peer_id] = available_stake - slash_amount
        else:
            slash_amount = 0.0

        self._settled_job_ids.add(job_id)
        record = {
            "job_id": job_id,
            "provider_peer_id": provider_peer_id,
            "amount": amount,
            "slashed": slashed,
            "slash_amount": slash_amount,
            "fully_covered": slash_amount >= amount if slashed else True,
        }
        self.records.append(record)
        return record

    def total_cost(self) -> float:
        """Sum of amounts actually paid out (excludes slashed jobs)."""
        return sum(r["amount"] for r in self.records if not r["slashed"])

    def export_csv(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["job_id", "provider_peer_id", "amount", "slashed", "slash_amount", "fully_covered"]
            )
            writer.writeheader()
            writer.writerows(self.records)


def centralized_cost(num_jobs: int, tokens_per_job: int, price_per_1k_tokens: float) -> float:
    """Theoretical cost of running the same workload against a hosted API, for the cost experiment."""
    return num_jobs * (tokens_per_job / 1000) * price_per_1k_tokens


def run_demo_scenario():
    """Registers 3 peers, settles a mix of pass/fail jobs, and compares cost vs. a centralized baseline."""
    ledger = SimulatedLedger()
    for peer_id in ["peer-1", "peer-2", "peer-3"]:
        ledger.register_stake(peer_id, 10.0)

    jobs = [
        ("job-1", "peer-1", 0.5, "pass"),
        ("job-2", "peer-2", 0.5, "pass"),
        ("job-3", "peer-1", 0.5, "fail"),  # peer-1 gets slashed
        ("job-4", "peer-3", 0.5, "pass"),
    ]
    for job_id, peer_id, amount, verdict in jobs:
        record = ledger.settle(job_id, peer_id, amount, verdict)
        print(record)

    print("\nfinal stakes:", ledger.stakes)
    print("total settled cost (simulated):", ledger.total_cost())

    baseline = centralized_cost(num_jobs=len(jobs), tokens_per_job=256, price_per_1k_tokens=0.002)
    print("theoretical centralized cost for same workload:", baseline)

    ledger.export_csv("../docs/results/settlement_demo.csv")
    print("\nexported to docs/results/settlement_demo.csv")


def run_edge_case_checks():
    """Demonstrates insufficient-stake slashing and duplicate-settlement rejection."""
    ledger = SimulatedLedger()
    ledger.register_stake("peer-low-stake", 0.2)

    # Insufficient stake: slash amount is capped at whatever's left, not the full job amount.
    record = ledger.settle("job-underfunded", "peer-low-stake", amount=0.5, verdict="fail")
    print("insufficient stake case:", record)
    assert record["slash_amount"] == 0.2
    assert record["fully_covered"] is False
    assert ledger.stakes["peer-low-stake"] == 0.0

    # Duplicate settlement: second attempt on the same job_id must be rejected.
    ledger.register_stake("peer-2", 10.0)
    ledger.settle("job-x", "peer-2", amount=0.5, verdict="pass")
    try:
        ledger.settle("job-x", "peer-2", amount=0.5, verdict="pass")
        raise AssertionError("expected DuplicateSettlementError")
    except DuplicateSettlementError as e:
        print("duplicate settlement correctly rejected:", e)


if __name__ == "__main__":
    run_demo_scenario()
    print("\n--- edge case checks ---")
    run_edge_case_checks()
