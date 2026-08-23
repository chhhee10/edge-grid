# Experiments (run Day 4)

These are the four experiments that produce the numbers for the paper's results section. Owned by the verification/evaluation track, but every track should log the metrics its component touches.

## 1. Latency (Time-To-First-Token)
Compare TTFT across your P2P nodes vs. calling a hosted API (any public OpenAI-compatible endpoint) as the centralized baseline.
- Metric: TTFT in ms, N requests, report mean/median/p95.
- Owner: inference + discovery (P2P adds routing/discovery overhead on top of raw inference).

## 2. Auction convergence time
Measure how long the sealed-bid GossipSub auction takes to converge as node count increases (3 → 5 nodes).
- Metric: wall-clock time from job broadcast to bid selection, per node count.
- Owner: discovery.

## 3. Validator accuracy
Inject N deliberately bad/hallucinated outputs into the pipeline; measure the LLM-as-judge validator's detection rate (precision/recall).
- Metric: TP/FP/TN/FN against a labeled set (use the TruthfulQA subset + your own injected bad outputs).
- Owner: verification.

## 4. Cost
Compare simulated settlement "cost" (e.g. token-weighted local ledger cost) vs. a theoretical centralized $/token rate for the same workload.
- Metric: $/1k tokens, simulated vs. centralized baseline.
- Owner: settlement (contracts/) + verification for write-up.

## Reporting
Log raw results as CSV/JSON in this repo (e.g. `docs/results/`) so the paper's tables/plots can be regenerated. Note any dropped/skipped cases explicitly — don't silently under-report N.
