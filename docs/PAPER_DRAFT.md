# The Edge Grid: A Prototype for Decentralized Peer-to-Peer AI Inference

*Draft — [fill in names], [fill in course/venue]*

---

## Abstract
*(write last — 150-200 words summarizing problem, approach, and key result)*

[TODO after experiments]: We present The Edge Grid, a small-scale prototype of a decentralized peer-to-peer network for AI inference. Unlike centralized inference services, our system allows participating nodes to discover one another, bid on inference jobs, execute them locally, and have their outputs independently verified before settlement — without a central authority. We implement and evaluate a 4-node prototype using [py-libp2p / Ollama / LLM-as-judge], measuring [latency, auction convergence, judge accuracy, cost]. Our results show [TODO]. We discuss the architecture's limitations at this scale and outline the path to a production-grade system.

---

## 1. Introduction

**Motivation:** Centralized AI inference (e.g., hosted APIs like OpenAI, Anthropic) concentrates control, cost, and trust in a single provider. This raises concerns around [pricing power / single point of failure / data governance / access for underserved regions — pick what fits your framing].

**Problem statement:** Can a decentralized network of commodity machines provide AI inference with (a) acceptable latency, (b) a working economic incentive mechanism, and (c) reliable output verification — without centralized infrastructure?

**Contribution:** We design and implement The Edge Grid, combining four previously-separate mechanisms — P2P peer discovery, sealed-bid job auctions, local LLM inference, and LLM-as-judge output verification with simulated economic settlement — into one working small-scale prototype, and report experimental results validating the architecture.

**Scope note (state explicitly, don't bury this):** This is a research prototype, not a production system. We deliberately scoped down from a full blockchain-settled, GPU-accelerated design (see Section 3.2) to something buildable and testable in [5 days / your actual timeframe] by a small team.

---

## 2. Related Work

*(Fill in from the earlier repo research — cite properly if this becomes a real submission)*

- **hyperspace-node** — decentralized P2P AI inference on libp2p using GossipSub + Kademlia DHT, with a reward system for presence/useful work. Closest architectural analog to our discovery + market layer.
- **Morpheus-Lumerin-Node** — blockchain-settled AI marketplace on Arbitrum L2; providers bid via smart contract, proxy-router handles routing. Reference for our settlement design (simulated in our prototype; see 3.2).
- **conduit** — P2P LLM sharing over rust-libp2p with Kademlia DHT-based model discovery, OpenAI-compatible API. Reference for our discovery layer's routing pattern.
- **KwaaiNet** — trust-gated routing by model/trust/latency across libp2p, distributed inference with session-pinned peer paths.

**Positioning:** No existing system we found combines DHT-based discovery, a sealed-bid auction market, local LLM inference, LLM-as-judge verification, and economic settlement in one evaluated system. Each existing project implements a subset. Our contribution is the integration and empirical evaluation, not any single novel mechanism.

---

## 3. System Design

### 3.1 Architecture Overview
Four components, chained as: **discovery → auction → inference → verification → settlement**.

*(Insert an architecture diagram here — box-and-arrow: Requester node → GossipSub job broadcast → N provider nodes bid → winning node runs inference → judge node verifies → settlement ledger updates)*

1. **Discovery + Market Protocol** — nodes join a Kademlia DHT for peer discovery; a GossipSub topic carries job broadcasts and sealed bids; the requester selects a winner by [price / estimated latency].
2. **Edge Inference Engine** — the winning node runs the job locally via Ollama (quantized small model), returns output + a hash commitment of the result.
3. **Agentic Verification** — an independent LLM-as-judge scores the output pass/fail for correctness/hallucination against a reference dataset subset.
4. **Settlement** — a ledger (simulated in this prototype) tracks staked collateral per node; a failed verification slashes the provider's stake.

Message schemas for each hop are fixed and documented (see `shared/schemas.md` in the repo) to keep components independently testable.

### 3.2 Prototype-Scale Limitations (state honestly — this is expected and fine in a prototype paper)

| Full design | Prototype implementation | Why cut |
|---|---|---|
| Arbitrum Stylus (Rust/WASM) contracts | Solidity design sketches only, not deployed | Team had no blockchain specialist; 5-day timeline |
| Celestia data availability | On-chain-style SHA-256 hash commitment only | Out of scope for prototype |
| vLLM on GPU infrastructure | Ollama, CPU-only, single small quantized model | No GPU budget; needed to run on laptops |
| Real economic staking/slashing | Simulated stake in a local ledger | No real funds/testnet deployment in scope |
| Fine-tuned LLM judge | Off-the-shelf small model as judge | No fine-tuning data/time available |

This table should appear near-verbatim in the paper's limitations section — it's honest, and comparable systems in our related work (Section 2) report similar scope reductions at prototype stage.

---

## 4. Evaluation

*(Full spec lives in `docs/EXPERIMENTS.md` — pull the methodology text from there almost verbatim)*

### 4.1 Experimental Setup
- N nodes: [TODO — how many laptops/machines you actually tested on]
- Model: [Qwen2.5-1.5B / Llama-3.2-3B — whichever you used]
- Judge model: [same or different model]
- Dataset: TruthfulQA subset, n=[TODO]

### 4.2 Results

**Latency (TTFT).** [TODO: table/plot — P2P nodes vs. centralized hosted API baseline, mean/median/p95]

**Auction convergence.** [TODO: table/plot — convergence time as node count goes 3→5]

**Verification accuracy.** [TODO: table — precision/recall on injected bad outputs vs. TruthfulQA subset]

**Cost.** [TODO: table — simulated settlement cost vs. theoretical centralized $/token for same workload]

### 4.3 Discussion
[TODO after results are in — interpret what surprised you, what confirms the architecture works, what doesn't scale]

---

## 5. Limitations and Future Work
- Prototype scale (N=[TODO] nodes) — production scaling, network churn, and adversarial nodes are unaddressed.
- No real economic stakes — sybil resistance and rational-actor incentive analysis are future work.
- Judge model not fine-tuned — accuracy numbers are a lower bound; a fine-tuned judge would likely perform better.
- No on-chain deployment — real gas costs, contract security, and settlement finality under network partition are unverified.

---

## 6. Conclusion
[TODO — 3-4 sentences, mirror the abstract, state the core validated claim plainly: "we show that X is achievable in a small-scale prototype; production deployment remains future work."]

---

## Writing checklist (day 5 workflow)
- [ ] Fill Section 4 tables/plots from `docs/results/*.csv`
- [ ] Write Discussion (4.3) once numbers are in
- [ ] Write Abstract + Conclusion last, once everything else is final
- [ ] Add architecture diagram (Section 3.1)
- [ ] Proper citations for Section 2 (replace bare repo names with actual citations if this is a formal submission)
- [ ] Spell-check, check page/word limit against submission requirements
