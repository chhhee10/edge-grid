"""
Local settlement simulation — the actual settlement logic used in the demo.

Mirrors the staking/escrow/slashing rules sketched in contracts/*.sol, without
requiring deployment. See ../shared/schemas.md for the settlement_record shape.
"""


class SimulatedLedger:
    def __init__(self):
        self.stakes: dict[str, float] = {}
        self.records: list[dict] = []

    def register_stake(self, peer_id: str, amount: float):
        self.stakes[peer_id] = self.stakes.get(peer_id, 0.0) + amount

    def settle(self, job_id: str, provider_peer_id: str, amount: float, verdict: str) -> dict:
        slashed = verdict == "fail"
        if slashed:
            self.stakes[provider_peer_id] = max(0.0, self.stakes.get(provider_peer_id, 0.0) - amount)
        record = {
            "job_id": job_id,
            "provider_peer_id": provider_peer_id,
            "amount": amount,
            "slashed": slashed,
        }
        self.records.append(record)
        return record

    def total_cost(self) -> float:
        return sum(r["amount"] for r in self.records if not r["slashed"])


if __name__ == "__main__":
    ledger = SimulatedLedger()
    ledger.register_stake("peer-1", 10.0)
    print(ledger.settle(job_id="test", provider_peer_id="peer-1", amount=0.5, verdict="pass"))
    print("stakes:", ledger.stakes)
