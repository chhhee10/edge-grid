# Settlement (Simulated)

**Scope cut for the 5-day timeline:** these Solidity contracts are design artifacts for the paper's architecture section — they are NOT deployed and NOT wired into the demo. The actual settlement logic used in the working prototype is `simulate.py`, a local Python ledger with the same staking/slashing rules.

## Reference
[Morpheus-Lumerin-Node](https://github.com/MorpheusAIs/Morpheus-Lumerin-Node) — proxy-router + escrow contract structure (study the *pattern*: bid → escrow → settle → slash).

## Deliverable
- `simulate.py`: local ledger simulating stake, escrow, settlement, and slashing — this is what the demo actually calls.
- `contracts/*.sol`: Solidity sketches matching the same logic, included in the paper as the production-path design (not deployed).

## Day 1 TODO
- [ ] Get `simulate.py` running standalone with a fake job → settle → slash flow.
- [ ] Agree on settlement_record schema with verification track (see `../shared/schemas.md`).

## Experiment owned
Cost: simulated settlement cost vs. theoretical centralized $/token — see `../docs/EXPERIMENTS.md`.
