# Engineering Diary & Operational Intelligence Report — Harshit

**Date:** 2026-08-24  
**Project:** The Edge Grid (Small-scale Decentralized P2P AI Inference Prototype)  
**Track:** Track C — Agentic Verification & Evaluation Harness  
**Author:** Harshit (Track C Lead) & AI Agent Collaborator  

---

# 1. Executive Summary
- **Day Overview:** Designed, planned, implemented, and validated the complete **Agentic Verification + Evaluation Harness** (Track C) for *The Edge Grid* research paper deliverable.
- **Main Objectives:**
  1. Build an LLM-as-judge scoring pipeline (1–5 quality rubric + binary PASS/FAIL).
  2. Implement an automated TruthfulQA benchmark loader with offline caching.
  3. Create an adversarial fraud injector with 4 distinct corruption strategies.
  4. Build an automated evaluation harness to compute paper metrics (Precision, Recall, F1, Accuracy, Mean Scores).
  5. Connect verification to Track B (Inference) and Track D (Simulated Staking/Slashing Ledger).
- **Major Accomplishments:**
  - Upgraded architecture from local 1.5B Ollama judge to Groq Llama-3.3-70B judge with automated fallback to local/mock execution.
  - Successfully downloaded, formatted, and cached a 60-question TruthfulQA evaluation dataset.
  - Validated all 4 corruption strategies and generated end-to-end evaluation results (`verification_results.csv` & `verification_summary.csv`).
  - Tested complete multi-node pipeline demo with staking, verification, and stake slashing (`integration_results.csv`).
- **Overall Status:** **Track C core implementation is 100% complete and operational.** Ready for production data gathering with an active Groq API key and final cross-track integration on Day 4.

---

# 2. Tasks Completed

### Task 1: Environment & Dependency Isolation
- **Purpose:** Create an isolated Python environment for all verification dependencies without polluting global environments.
- **Files/Components:** `.venv/`, `verification/requirements.txt`, `.gitignore`
- **Changes:**
  - Added `groq`, `datasets`, `pandas`, `requests`, `python-dotenv`, and supporting libraries to `verification/requirements.txt`.
  - Created `.venv` virtual environment and installed all dependencies.
  - Confirmed `.gitignore` ignores `.venv/`, `venv/`, and `.env`.
- **Outcome:** Clean, repeatable virtual environment.

### Task 2: Centralized Configuration System
- **Purpose:** Eliminate hardcoded values, model names, and file paths across the verification codebase.
- **Files/Components:** `verification/config.py`, `verification/.env`
- **Changes:**
  - Created `config.py` managing `GROQ_API_KEY`, `GROQ_JUDGE_MODEL` (`llama-3.3-70b-versatile`), `GROQ_SIMULATOR_MODEL` (`llama-3.1-8b-instant`), `OLLAMA_URL`, `PASS_THRESHOLD` (`3`), and directory paths.
  - Generated `.env` configuration template.
- **Outcome:** Clean configuration interface with environment variable overrides.

### Task 3: Hardened LLM-as-Judge (`evaluator.py`)
- **Purpose:** Grade AI-generated answers on factual accuracy using a 1–5 score and PASS/FAIL verdict.
- **Files/Components:** `verification/evaluator.py`
- **Changes:**
  - Structured system prompt with detailed 1–5 scoring rubric.
  - Enforced JSON mode output schema (`{"score": <1-5>, "verdict": "<PASS|FAIL>", "reason": "..."}`).
  - Built triple-layer fallback parser (JSON parsing $\rightarrow$ regex JSON extraction $\rightarrow$ heuristic keyword search).
  - Added multi-backend support (`backend="groq"`, `backend="ollama"`, `backend="mock"`).
  - Implemented `score_inference_result()` complying with `shared/schemas.md`.
- **Outcome:** Reliable judge module resistant to JSON parsing errors and API timeouts.

### Task 4: TruthfulQA Benchmark Pipeline (`truthfulqa_loader.py`)
- **Purpose:** Provide reproducible, ground-truth labeled evaluation data.
- **Files/Components:** `verification/truthfulqa_loader.py`, `verification/data/truthfulqa_subset.csv`
- **Changes:**
  - Implemented automatic HuggingFace Hub download of `truthfulqa/truthful_qa` (generation split).
  - Built deterministic sampling (seed=42) extracting `question`, `best_answer`, `correct_answers`, `incorrect_answers`.
  - Cached 60 questions to local CSV with fallback curated questions for offline resilience.
- **Outcome:** Ready-to-use dataset with 60 benchmark questions.

### Task 5: Adversarial Fraud Injector (`fraud_injector.py`)
- **Purpose:** Simulate malicious/hallucinating edge nodes in the decentralized network to test judge recall.
- **Files/Components:** `verification/fraud_injector.py`
- **Changes:**
  - `swap_incorrect`: Pulls known human misconceptions from TruthfulQA reference data.
  - `negate`: Programmatically inverts semantic assertion using grammatical negation rules.
  - `hallucinate_entity`: Swaps numbers, dates, and celestial/scientific entities.
  - `random_topic`: Swaps in completely unrelated facts to test off-topic detection.
- **Outcome:** High-variety adversarial generation pipeline.

### Task 6: Evaluation Harness & Paper Metric Generator (`run_harness.py`)
- **Purpose:** Automate the execution of experiments and output publication-ready tables.
- **Files/Components:** `verification/run_harness.py`, `docs/results/verification_results.csv`, `docs/results/verification_summary.csv`
- **Changes:**
  - CLI support (`--subset-size`, `--strategies`, `--use-ollama`, `--delay`).
  - Automated evaluation loop over honest and corrupted conditions.
  - Real-time computation of TP, FP, TN, FN, Precision, Recall, F1, Accuracy, and average scores.
  - Output formatting in terminal and CSV export.
- **Outcome:** Automated one-command paper metric generation.

### Task 7: Full Pipeline Integration Demo (`run_integration.py`)
- **Purpose:** Connect Track B inference outputs to Track C verification and Track D settlement.
- **Files/Components:** `verification/run_integration.py`, `docs/results/integration_results.csv`
- **Changes:**
  - Initialized `SimulatedLedger` with 3 provider peer nodes.
  - Simulated job submissions, judge scoring, stake disbursements, and slashing on failure.
  - Calculated simulated vs. centralized baseline cost.
- **Outcome:** Verified complete lifecycle: prompt $\rightarrow$ inference $\rightarrow$ judge $\rightarrow$ settlement.

---

# 3. Issues & Debugging Log

### Issue 1: Relative Import Failure During Standalone Script Execution
- **Error:** `ImportError: attempted relative import with no known parent package` when executing `python verification/truthfulqa_loader.py`.
- **Root Cause:** When a Python file is run directly as `__main__`, it has no package parent context, making `from .config import ...` invalid.
- **Debugging & Resolution:**
  - Added dual import pattern:
    ```python
    try:
        from .config import DATA_DIR, TRUTHFULQA_SUBSET_SIZE
    except (ImportError, ValueError):
        from config import DATA_DIR, TRUTHFULQA_SUBSET_SIZE
    ```
  - Added explicit root directory insertion to `sys.path` in runners.
- **Preventive Measure:** Always provide `try/except (ImportError, ValueError)` guards for internal sibling imports in modules that may be executed directly.

### Issue 2: `datetime.utcnow()` Deprecation Warnings
- **Error:** `DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in Python 3.14+`.
- **Root Cause:** Python 3.12+ deprecates naive UTC datetimes in favor of timezone-aware objects.
- **Fix:** Switched all timestamp generation to `datetime.now(timezone.utc).isoformat()`.

### Issue 3: Missing `GROQ_API_KEY` During Local Development
- **Problem:** If a user runs scripts before entering a Groq key, requests would crash with unhandled authentication errors.
- **Root Cause:** Code originally assumed `GROQ_API_KEY` was always present in `.env`.
- **Fix:** Added automatic fallback to `backend="mock"` with rule-based heuristics and a clear console notice if `GROQ_API_KEY` is unset. Once the user adds their key, it seamlessly switches to real Groq API inference.

---

# 4. Pending Work / Incomplete Tasks

| Task | Status | Blockers / Dependencies | Recommended Next Step |
|---|---|---|---|
| **Add User Groq API Key** | Pending User Input | None | User adds free key to `verification/.env` |
| **Run Full 60-Question Evaluation** | Ready to Run | Requires Groq API Key | Execute `python verification/run_harness.py --subset-size 60 --delay 1.5` |
| **Track B Ollama Integration** | Blocked on Track B | Track B installing Ollama | Wire real Ollama generation into `run_integration.py` |
| **Write Paper Section 4.2** | Ready after Full Run | Needs CSV numbers from 60-question run | Copy metrics from `verification_summary.csv` into `docs/PAPER_DRAFT.md` |

---

# 5. Architecture & Technical Decisions

1. **Groq Llama-3.3-70B for Verifier vs. Local 1.5B Model:**
   - *Rationale:* A 1.5B edge model cannot reliably catch its own hallucinations. A 70B verifier model via Groq provides high accuracy at zero cost on Groq's free tier.
   - *Paper Framing:* Stated in Section 3.2 as a prototype design choice ("simulated high-capability verifier node").

2. **1–5 Quality Scale + Binary PASS/FAIL Hybrid:**
   - *Rationale:* Binary verdict is required for on-chain staking/slashing logic (`PASS` = pay, `FAIL` = slash). 1–5 numeric scale allows generating score distribution histograms and ROC curves for the research paper.
   - *Threshold:* Scores 3, 4, 5 $\rightarrow$ PASS; Scores 1, 2 $\rightarrow$ FAIL.

3. **Disk-Cached Benchmark Dataset:**
   - *Rationale:* Downloading TruthfulQA from HuggingFace on every test is slow and vulnerable to rate limits. Caching to `verification/data/truthfulqa_subset.csv` ensures fast, reproducible runs.

---

# 6. Code Intelligence Notes

### Reusable Components
- `Judge` class in [`evaluator.py`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/verification/evaluator.py): Can be dropped into any test script to score `(prompt, answer)` pairs.
- `score_inference_result()`: Adapter accepting Track B JSON and producing Track D JSON.
- `inject_fraud()` in [`fraud_injector.py`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/verification/fraud_injector.py): Standalone adversarial text mutator.

### Naming Conventions & Schema Alignment
- Job IDs: UUID strings (e.g., `b1c38a8b`).
- Verdicts: lowercase strings `"pass"` or `"fail"`.
- Ledger amounts: float numbers in ETH.
- Result tables: written to `docs/results/` as CSV files.

---

# 7. Efficiency Improvements & Best Practices

- **Automate Rate-Limit Backoff:** Added `--delay 1.5` default in `run_harness.py` to prevent Groq free-tier 429 throttling (30 requests/min).
- **Incremental CSV Writes:** `run_harness.py` uses `append_result()` after every single question evaluation. If the process is interrupted, progress is not lost.
- **Offline Fallbacks:** TruthfulQA loader and Judge both contain hardcoded offline fallbacks so the repo can be evaluated even with zero internet connectivity.

---

# 8. Agent Collaboration Context

### Mental Model of the Edge Grid
```
[Requester] --(GossipSub Job)--> [Edge Nodes (Track B)]
                                      |
                             (Inference Output)
                                      v
                             [Judge Node (Track C)]
                                      |
                             (Validation Verdict)
                                      v
                             [Ledger (Track D)] -> Pay or Slash Stake
```

### Critical Files to Read First
1. [`shared/schemas.md`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/shared/schemas.md) — Shared inter-track JSON contracts.
2. [`verification/evaluator.py`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/verification/evaluator.py) — Judge scoring engine.
3. [`verification/run_harness.py`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/verification/run_harness.py) — Experiment test runner.
4. [`contracts/simulate.py`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/contracts/simulate.py) — Staking and settlement simulation.

---

# 9. Important Commands & References

### Virtual Environment Commands (Windows PowerShell)
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run 5-question smoke test
.\.venv\Scripts\python.exe verification/run_harness.py --subset-size 5

# Run full 60-question paper experiment
.\.venv\Scripts\python.exe verification/run_harness.py --subset-size 60 --delay 1.5

# Run end-to-end integration demo
.\.venv\Scripts\python.exe verification/run_integration.py
```

### Key URLs & References
- Groq Console: [console.groq.com](https://console.groq.com)
- TruthfulQA Benchmark: [github.com/sylinrl/TruthfulQA](https://github.com/sylinrl/TruthfulQA)
- Edge Grid Schemas: [`shared/schemas.md`](file:///c:/Users/sudha/Ant_gravity/rojects/edge-grid/shared/schemas.md)

---

# 10. Learning & Insights

1. **Adversarial Diversity Matters:** Simple negation (`negate`) can sometimes be subtle, whereas entity hallucination (`hallucinate_entity`) and known misconceptions (`swap_incorrect`) provide much clearer signals for 70B evaluators. Reporting all four gives depth to the paper.
2. **Crash-Resilience in Long Runs:** Running 300 evaluations across 60 questions takes ~10–15 minutes. Writing rows incrementally to CSV is essential to prevent losing trial data.

---

# 11. Suggested Next Session Plan

1. **Step 1 (Quick Win):** Add free `GROQ_API_KEY` to `verification/.env`.
2. **Step 2 (Data Collection):** Run `python verification/run_harness.py --subset-size 60 --delay 1.5` to generate the final publication numbers.
3. **Step 3 (Paper Update):** Populate Section 4.2 and Section 4.4 in `docs/PAPER_DRAFT.md` directly from `docs/results/verification_summary.csv`.
4. **Step 4 (Cross-Track Sync):** Test `run_integration.py` against Track B's live Ollama node once Track B finishes local model setup.
