# Agentic Verification + Evaluation Harness

Owns: LLM-as-judge validator + the evaluation harness that produces the paper's results tables.

**Highest priority track** — start the evaluation harness on Day 2, not Day 4. Everything else in the pipeline is only useful once it's logging metrics this harness can consume.

## Deliverable
- LLM-as-judge validator (off-the-shelf small model, no fine-tuning) that scores an inference_result as pass/fail.
- Scoring against a TruthfulQA subset (reuse whatever subset came out of the lit survey).
- Fraud injection: deliberately corrupt N outputs, measure detection rate.
- Logging: write every metric to `../docs/results/` as CSV/JSON as soon as it's available — don't wait until Day 4 to start collecting.

## Day 1 TODO
- [ ] `pip install -r requirements.txt`
- [ ] Pick the judge model (can be the same Ollama model as inference, or a different one for independence) and get a basic scoring call working.
- [ ] Pull the TruthfulQA subset into `verification/data/`.

## Experiments owned
Validator accuracy (precision/recall on injected bad outputs) — see `../docs/EXPERIMENTS.md`. Also coordinates the other 3 experiments' result logging.
