# References — Verification and Correction Record

**Project:** DePIN-Edge: "The Edge Grid" — A Decentralized Physical Infrastructure Network for
Localized, Verifiable AI Inference
**Department of CSE (IoT, Cyber-Security and Blockchain Technology), Sir M. Visvesvaraya Institute of
Technology, Bengaluru — VTU, Belagavi. Academic Year 2026–27.**

**Purpose of this document.** The Phase-1 Literature Survey and the Phase-1 presentation deck both
carry an identical twenty-entry reference list. Every entry in that list has been independently
verified against arXiv, Crossref, DBLP, the ACL Anthology, the ACM and IEEE digital libraries, the
PMLR proceedings and the publishers' own pages. The verification established that **eleven of the
twenty entries were materially incorrect** and that **two entries do not correspond to any real
publication**. Because a reference list that cannot survive an examiner's spot-check discredits the
work it supports, this document supersedes the Phase-1 list. The corrected list in Section 1 is the
list that must be reprinted in the Phase-1 report; the Phase-1 list must not be reused.

The numbering [1]–[20] has been preserved so that the existing in-text citation markers in the
Literature Survey continue to resolve. Two of those numbers, [5] and [7], previously pointed at
publications that do not exist; each has been re-pointed at a genuine source that actually supports
the claim the survey was making. Entries [21]–[28] are additions: systems and results that the
survey's research-gap argument depends on but never examined.

---

## 1. Corrected Reference List (IEEE style)

### Peer-to-peer networking and distributed systems foundations

[1] P. Maymounkov and D. Mazières, "Kademlia: A peer-to-peer information system based on the XOR
metric," in *Peer-to-Peer Systems: First International Workshop (IPTPS 2002)*, Cambridge, MA, USA,
Mar. 2002, Lecture Notes in Computer Science, vol. 2429, Berlin, Germany: Springer, 2002,
pp. 53–65. doi: 10.1007/3-540-45748-8_5.

[2] D. Vyzovitis, Y. Napora, D. McCormick, D. Dias, and Y. Psaras, "GossipSub: Attack-resilient
message propagation in the Filecoin and ETH2.0 networks," Protocol Labs, Technical Report, Jul. 2020.
[Online]. Available: https://arxiv.org/abs/2007.02754. arXiv:2007.02754.

[13] J. Benet, "IPFS — Content addressed, versioned, P2P file system (draft 3)," Protocol Labs,
Technical Report, Jul. 2014. [Online]. Available: https://arxiv.org/abs/1407.3561. arXiv:1407.3561.

[19] J. R. Douceur, "The Sybil attack," in *Peer-to-Peer Systems: First International Workshop
(IPTPS 2002)*, Cambridge, MA, USA, Mar. 2002, Lecture Notes in Computer Science, vol. 2429, Berlin,
Germany: Springer, 2002, pp. 251–260. doi: 10.1007/3-540-45748-8_24.

### Blockchain settlement, data availability and fraud proofs

[3] L. Bousfield, R. Bousfield, C. Buckland, B. Burgess, J. Colvin, E. W. Felten, S. Goldfeder,
D. Goldman, B. Huddleston, H. Kalodner, F. A. Lacs, H. Ng, A. Sanghi, T. Wilson, V. Yermakova, and
T. Zidenberg, "Arbitrum Nitro: A second-generation optimistic rollup," Offchain Labs, Inc.,
Whitepaper, Aug. 2022. [Online]. Available: https://docs.arbitrum.io/nitro-whitepaper.pdf

[4] M. Al-Bassam, A. Sonnino, and V. Buterin, "Fraud and data availability proofs: Maximising light
client security and scaling blockchains with dishonest majorities," University College London and
Ethereum Foundation, Preprint, Sep. 2018 (rev. May 2019). [Online]. Available:
https://arxiv.org/abs/1809.09044. arXiv:1809.09044.

[20] J. Teutsch and C. Reitwießner, "A scalable verification solution for blockchains," TrueBit
Whitepaper, Nov. 2017; also published in *Aspects of Computation and Automata Theory with
Applications*, Lecture Notes Series, Institute for Mathematical Sciences, National University of
Singapore, vol. 42, Singapore: World Scientific, 2023, pp. 377–424.
doi: 10.1142/9789811278631_0015. Preprint: arXiv:1908.04756.

### Proof of useful work and verifiable computation (replaces the fabricated [5])

[5a] M. Ball, A. Rosen, M. Sabin, and P. N. Vasudevan, "Proofs of useful work," IACR Cryptology
ePrint Archive, Report 2017/203, 2017. [Online]. Available: https://eprint.iacr.org/2017/203

[5b] M. Fitzi, A. Kiayias, G. Panagiotakos, and A. Russell, "Ofelimos: Combinatorial optimization via
proof-of-useful-work — A provably secure blockchain protocol," in *Advances in Cryptology — CRYPTO
2022*, Lecture Notes in Computer Science, vol. 13508, Cham, Switzerland: Springer, 2022,
pp. 339–369. doi: 10.1007/978-3-031-15979-4_12.

[5c] H. Jia, M. Yaghini, C. A. Choquette-Choo, N. Dullerud, A. Thudi, V. Chandrasekaran, and
N. Papernot, "Proof-of-Learning: Definitions and practice," in *Proc. 2021 IEEE Symposium on Security
and Privacy (SP)*, San Francisco, CA, USA, May 2021, pp. 1039–1056.
doi: 10.1109/SP40001.2021.00106.

### Inference runtimes

[6] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica,
"Efficient memory management for large language model serving with PagedAttention," in *Proc. 29th
ACM Symposium on Operating Systems Principles (SOSP '23)*, Koblenz, Germany, Oct. 2023, pp. 611–626.
doi: 10.1145/3600006.3613165.

[7a] Ollama Contributors, *Ollama* (version 0.x) [Computer software]. Ollama Inc., 2023–.
[Online]. Available: https://github.com/ollama/ollama

[7b] G. Gerganov and llama.cpp Contributors, *llama.cpp: LLM inference in C/C++* [Computer software].
2023–. [Online]. Available: https://github.com/ggml-org/llama.cpp

### LLM evaluation, judging and hallucination benchmarks

[8] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing,
H. Zhang, J. E. Gonzalez, and I. Stoica, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," in
*Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks
Track*, New Orleans, LA, USA, Dec. 2023. Preprint: arXiv:2306.05685.

[9] S. Lin, J. Hilton, and O. Evans, "TruthfulQA: Measuring how models mimic human falsehoods," in
*Proc. 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers)*, Dublin, Ireland, May 2022, pp. 3214–3252. doi: 10.18653/v1/2022.acl-long.229.

[11] W.-L. Chiang, L. Zheng, Y. Sheng, A. N. Angelopoulos, T. Li, D. Li, B. Zhu, H. Zhang, M. I.
Jordan, J. E. Gonzalez, and I. Stoica, "Chatbot Arena: An open platform for evaluating LLMs by human
preference," in *Proc. 41st International Conference on Machine Learning (ICML 2024)*, Vienna,
Austria, Jul. 2024, PMLR, vol. 235, pp. 8359–8388. Preprint: arXiv:2403.04132.

### Decentralized and edge LLM inference systems

[10] A. Borzunov, D. Baranchuk, T. Dettmers, M. Ryabinin, Y. Belkada, A. Chumachenko, P. Samygin, and
C. Raffel, "Petals: Collaborative inference and fine-tuning of large models," in *Proc. 61st Annual
Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations)*, Toronto,
Canada, Jul. 2023, pp. 558–568. doi: 10.18653/v1/2023.acl-demo.54.

[10b] A. Borzunov, M. Ryabinin, A. Chumachenko, D. Baranchuk, T. Dettmers, Y. Belkada, P. Samygin,
and C. Raffel, "Distributed inference and fine-tuning of large language models over the Internet," in
*Advances in Neural Information Processing Systems 36 (NeurIPS 2023)*, New Orleans, LA, USA,
Dec. 2023, pp. 12312–12331. Preprint: arXiv:2312.08361.

[12] DGrid Research Team, "DGrid AI: The decentralized AI smart network," DGrid Litepaper, ver. June
2025. [Online]. Available: https://static.dgrid.ai/dgrid_litepaper.pdf

[14] C. Tong, Y. Jiang, G. Chen, T. Zhao, S. Lu, W. Qu, E. Yang, L. Ai, and B. Yuan, "Parallax:
Efficient LLM inference service over decentralized environment," Preprint, Sep. 2025. [Online].
Available: https://arxiv.org/abs/2509.26182. arXiv:2509.26182.

[15] Y. Yang, A. Merlina, W. Song, T. Yuan, K. Birman, and R. Vitenberg, "Navigator: A decentralized
scheduler for latency-sensitive AI workflows," in *Proc. 2024 IEEE International Conference on Edge
Computing and Communications (EDGE)*, Shenzhen, China, Jul. 2024, pp. 35–47.
doi: 10.1109/EDGE62653.2024.00015.

[16] H. Liu, J. Cao, B. Yang, D. Bai, Y. Cao, X. Shen, Y. Zhang, J. Liang, S. Jiang, and M. Zhang,
"PolyLink: A blockchain based decentralized edge AI platform for LLM inference," Preprint, Oct. 2025.
[Online]. Available: https://arxiv.org/abs/2510.02395. arXiv:2510.02395.

[17] H. Zhang, Y. Zhao, C. Angione, H. Yang, J. Buban, A. Farhan, F. Johnston, and P. Colangelo,
"Towards secure and private AI: A framework for decentralized inference," in *Proc. NeurIPS 2024
Workshop on Responsibly Building the Next Generation of Multimodal Foundational Models (RBFM)*,
Vancouver, Canada, Dec. 2024. Preprint: arXiv:2407.19401.

[18] Z. Cheng, R. Sun, J. Sun, and Y. Guo, "Scaling decentralized learning with FLock," Preprint,
Jul. 2025 (rev. Aug. 2025). [Online]. Available: https://arxiv.org/abs/2507.15349. arXiv:2507.15349.

---

## 2. Additions — Systems the Survey Must Examine

The Phase-1 survey concludes that "no existing system integrates all five [components] into a
single, open, economically self-sustaining, blockchain-verified, latency-optimized … decentralized AI
inference network." That claim is compared only against Petals, PolyLink, DGrid, Parallax, Navigator,
Nesa and FLock — all of them research artefacts. It is not compared against a single one of the
decentralised-compute networks that are actually in production and selling inference today. A
research-gap claim is only as strong as the systems it was tested against, and an examiner familiar
with the DePIN sector will name Bittensor, Akash or Morpheus within the first minute of questioning.
The following eight references close that exposure.

**Morpheus/Lumerin is the most urgent of these.** It is an Arbitrum-L2-settled AI inference
marketplace in which compute providers post bids that smart contracts match — that is, the exact
mechanism this project claims as its contribution. The project's own repository README (`README.md`,
line 19) and design draft (`docs/PAPER_DRAFT.md`, line 31) already cite it as the reference
implementation for `contracts/`. The Literature Survey has never mentioned it. That gap between what
the code was built from and what the survey admits to reading is the single most damaging
inconsistency in the Phase-1 package, and it must be closed before submission.

[21] Morpheus, Trinity, and Neo (pseudonymous), "Morpheus: A network for powering smart agents,"
Morpheus Whitepaper, Sep. 2023. [Online]. Available:
https://github.com/MorpheusAIs/Docs/blob/main/!KEYDOCS%20README%20FIRST!/WhitePaper.md

[22] MorpheusAIs, *Morpheus-Lumerin-Node: Proxy-router and inference marketplace node* [Computer
software]. 2024–. [Online]. Available: https://github.com/MorpheusAIs/Morpheus-Lumerin-Node

[23] E. Lui and J. Sun, "Bittensor protocol: The Bitcoin in decentralized artificial intelligence? A
critical and empirical analysis," in *Mathematical Research for Blockchain Economy: 6th International
Conference (MARBLE 2025)*, Athens, Greece, Lecture Notes in Operations Research, Cham, Switzerland:
Springer, 2026, pp. 145–165. doi: 10.1007/978-3-032-13377-9_7. Preprint: arXiv:2507.02951.

[24] Y. Rao, J. Steeves, A. Shaabana, D. Attevelt, and M. McAteer, "BitTensor: A peer-to-peer
intelligence market," Opentensor Foundation, Whitepaper, Mar. 2020 (rev. Nov. 2021; arXiv version
subsequently withdrawn). [Online]. Available: https://bittensor.com/whitepaper

[25] G. Osuri and A. Bozanich, "AKT: Akash network token and mining economics," Overclock Labs,
Economic Whitepaper, Mar. 2020. [Online]. Available:
https://akash-web-prod.s3.amazonaws.com/uploads/2020/03/akash-econ.pdf

[26] Golem Factory GmbH, "The Golem project: Crowdfunding whitepaper," Nov. 2016. [Online].
Available: https://assets.website-files.com/62446d07873fde065cbcb8d5/62446d07873fdeb626bcb927_Golemwhitepaper.pdf

[27] Gensyn AI Ltd., "Gensyn litepaper: A protocol for verifiable machine learning compute,"
Technical Report, 2022 (legacy edition). [Online]. Available: https://docs.gensyn.ai/litepaper

[28] Z. Lin, T. Wang, L. Shi, S. Zhang, and B. Cao, "Decentralized physical infrastructure network
(DePIN): Challenges and opportunities," Preprint, Jun. 2024. [Online]. Available:
https://arxiv.org/abs/2406.02239. arXiv:2406.02239.

[29] M. S. Andrew and M. C. Ballandies, "Are you a DePIN? A decision tree to classify decentralized
physical infrastructure networks," Preprint, Jan. 2025. [Online]. Available:
https://arxiv.org/abs/2501.17416. arXiv:2501.17416.

---

## 3. Corrections Applied

| Ref | As cited in Phase-1 | Verified fact | Status |
|:--|:--|:--|:--|
| [1] | "in Proc. IPTPS, Springer LNCS vol. 2429, **2020**" | IPTPS **2002**, LNCS 2429, pp. 53–65, doi 10.1007/3-540-45748-8_5 | Wrong year (off by 18 years) |
| [2] | "in Proc. **IEEE International Conference on Peer-to-Peer Computing (P2P), 2022**" | Protocol Labs technical report, arXiv:2007.02754, **Jul. 2020**. IEEE P2P has no 2022 edition — per DBLP its final edition was P2P 2015 | Wrong venue and year; cited venue did not exist |
| [3] | "H. **Kalodner** et al., … Offchain Labs Technical Report, **in Proc. IEEE Blockchain Conference, 2023**" | Offchain Labs whitepaper, **Aug. 2022**; sixteen authors, first author **L. Bousfield** — Kalodner is tenth. No IEEE Blockchain publication exists. (Kalodner *is* first author of the earlier "Arbitrum: Scalable, Private Smart Contracts," USENIX Security 2018 — the two papers appear to have been conflated) | Wrong authors, venue and year |
| [4] | "in Proc. **ACM CCS, 2023**" | arXiv:1809.09044, **Sep. 2018** (rev. May 2019). Never published at ACM CCS | Wrong venue and year |
| [4]† | Survey **table** row 4 describes this as "Celestia: A Modular Data Availability Network … (Al-Bassam et al., **Protocol Labs** / ACM CCS, 2023)" | The reference list and the table describe **two different papers**. The Celestia/LazyLedger design is a separate Al-Bassam work; Al-Bassam is UCL/Celestia Labs, not Protocol Labs | Internal inconsistency; table row must be rewritten to match [4] |
| [5] | "S. Balaji et al., 'Proof-of-Useful-Work: Repurposing Distributed Compute for AI Tasks,' IEEE Blockchain Conference, MIT Digital Currency Initiative, 2023" | **No such publication.** Absent from IEEE Xplore, the MIT DCI publication list, DBLP, Semantic Scholar and Google Scholar. No author "S. Balaji" is associated with any PoUW work | **Fabricated** — replaced by [5a], [5b], [5c] |
| [6] | "in Proc. ACM SOSP, 2023" | SOSP '23, Koblenz, pp. 611–626, doi 10.1145/3600006.3613165 | Correct (page range and DOI added) |
| [7] | "T. Eloundou et al., 'Ollama: Democratizing Local LLM Deployment on Consumer Hardware,' Springer AI & Society, vol. 39, no. 2, pp. 544–560, 2024" | **No such publication.** Ollama has never been described in a peer-reviewed paper; the repository has no `CITATION.cff` and issue #10906 is an open request for one. T. Eloundou is a genuine OpenAI researcher whose work ("GPTs are GPTs," *Science*, 2024) concerns labour-market impact and is unrelated to local inference runtimes. The volume, issue and page range are invented | **Fabricated** — replaced by software citations [7a], [7b] |
| [8] | "in Proc. NeurIPS, 2023" | NeurIPS 2023 **Datasets and Benchmarks Track**; arXiv:2306.05685 | Correct (track specified) |
| [8]† | Survey **table** row 8 titles this "LLM-as-a-Judge: Using Language Models to Evaluate Language Model Outputs" | Actual title is "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" | Table title invented; must match [8] |
| [9] | "in Proc. ACL, 2022" | ACL 2022, pp. 3214–3252, doi 10.18653/v1/2022.acl-long.229 | Correct (pages and DOI added) |
| [10] | "in Proc. **NeurIPS**, 2023" | **ACL 2023 System Demonstrations**, pp. 558–568, doi 10.18653/v1/2023.acl-demo.54. A *different* Borzunov et al. paper — "Distributed Inference and Fine-tuning of LLMs Over The Internet" — was at NeurIPS 2023; the two appear to have been merged | Wrong venue; NeurIPS paper added as [10b] |
| [11] | "in Proc. **ICLR**, 2024" | **ICML 2024**, PMLR vol. 235, pp. 8359–8388 | Wrong venue |
| [12] | DGrid Litepaper, June 2025 | URL returns HTTP 200; document is a corporate litepaper, not peer-reviewed | Exists; must be labelled a non-peer-reviewed industry document |
| [13] | "arXiv:1407.3561, **2021**" and, in the table, "arXiv **+ Springer**" | **Jul. 2014**. Never published by Springer; it is a Protocol Labs draft-3 preprint only | Wrong year; false publisher claim |
| [14] | arXiv:2509.26182, 2025 | Confirmed, Sep. 2025, nine authors as listed | Correct (table's title variant "…over Decentralized Heterogeneous GPU Environments" must be corrected to the real title) |
| [15] | "in Proc. IEEE EDGE, 2024" | IEEE EDGE 2024, Shenzhen, pp. 35–47, doi 10.1109/EDGE62653.2024.00015 | Correct (attribution should read Cornell **and University of Oslo**, not Cornell alone) |
| [16] | "arXiv:2510.02395, **IEEE**, 2025" | Confirmed arXiv preprint, Oct. 2025. **No IEEE publication.** The survey calls it "the closest **peer-reviewed** academic parallel" and "the most directly comparable peer-reviewed academic system" — it has not been peer-reviewed | Correct identifier; false venue and false peer-review claim |
| [17] | "Nesa Research, in Proc. NeurIPS RBFM Workshop, arXiv:2407.19401, 2024" | Confirmed: NeurIPS 2024 Workshop RBFM poster; arXiv:2407.19401, Jul. 2024 | Correct |
| [18] | "**Y. Chen** et al., 'Scaling Decentralized Learning with FLock: **Blockchain-Based Trust Layer for Collaborative LLM Fine-Tuning**,' arXiv:2507.15349, 2025" | Authors are **Z. Cheng, R. Sun, J. Sun and Y. Guo** — no author named Y. Chen. Real title is "Scaling Decentralized Learning with FLock"; the subtitle after the colon is invented. The 68 % ASR-reduction figure the survey quotes **is genuine** (verified in the paper's abstract and §5) | Wrong authors; invented subtitle |
| [19] | "in Proc. IPTPS, Springer LNCS, **2022**" | IPTPS **2002**, LNCS 2429, pp. 251–260, doi 10.1007/3-540-45748-8_24 | Wrong year (off by 20 years) |
| [19]† | Survey **table** row 19 titles it "The Sybil Attack in Permissionless Peer-to-Peer Networks" and claims it "evaluates proof-of-work, economic staking, and hardware attestation" | Real title is "The Sybil Attack." A 2002 paper predates economic staking and blockchain hardware attestation entirely and discusses none of them | Table title invented; content claim anachronistic and must be removed |
| [20] | "'…: **Optimistic Fraud Proofs**,' **Springer Cryptography, 2022**" | Real title is "A scalable verification solution for blockchains" (the TrueBit whitepaper), Nov. 2017; arXiv:1908.04756, 2019; book-chapter version is **World Scientific**, 2023, pp. 377–424, doi 10.1142/9789811278631_0015 — not Springer | Wrong title, publisher and year |
| [20]† | Survey **table** row 20 titles it "Optimistic Rollup Fraud Proofs: Interactive Verification for Off-Chain Computation" | Not the paper's title | Table title invented |

† = discrepancy between the survey's Table 1 row and its own reference list entry.

**Tally.** Of twenty entries: **five are correct** as cited ([6], [9], [14], [15], [17], with page
ranges and DOIs added here); **eleven carry a wrong venue, year, author list or title**; **two are
fabricated** ([5], [7]); and **two more** ([12], [16]) are real documents misrepresented as
peer-reviewed. Six of the twenty table rows additionally carry a paper title that does not match the
paper.

---

## 4. Consequences for the Argument, and Actions Required

**4.1 The economic premise currently rests on nothing.** Reference [5] is the sole citation for the
project's entire economic model — the claim that idle consumer GPU cycles can be monetised through
verifiable useful work rather than wasteful hashing. That citation is fabricated. The claim itself is
sound and well supported in the real literature, but it must be re-grounded. Ball et al. [5a]
establish that proofs of work can be built on problems of genuine computational interest; Fitzi et
al. [5b] give the first provably secure blockchain protocol whose consensus mechanism is a useful
optimisation solver; and Jia et al. [5c] supply what the project actually needs and [5] merely
claimed — a formal definition of proving that a specific machine-learning computation was performed.
Section 5c is the closest genuine antecedent to the Agentic Verification Module and should be cited
wherever the report currently cites [5].

**4.2 Ollama must be cited as software, not as scholarship.** Ollama has no paper. Any statement in
the report attributed to [7] — Apple Silicon throughput, GGUF quantisation behaviour, TTFT
benchmarks — is unsupported by a citable source and must instead be supported by **this project's own
measurements**, which is in fact the stronger position: the report has real numbers (≈624–730 ms warm
TTFT, ≈9,398 ms cold, CPU-only, no NVIDIA GPU) that no cited paper could supply. Cite [7a] and [7b]
for the software itself and the project's own runlogs for the performance claims.

**4.3 Two "peer-reviewed" comparators are preprints.** PolyLink [16] and Parallax [14] are arXiv
preprints, and DGrid [12] is a corporate litepaper. The survey leans on PolyLink as "the closest
peer-reviewed academic parallel," which is not true. The comparison remains valuable — these are the
right systems to compare against — but each must be labelled by what it is. An examiner who checks
one arXiv link and finds no venue will discount every other claim in the chapter.

**4.4 The research-gap claim is not yet defensible.** The "no existing system combines these"
argument was tested against seven research prototypes and zero production networks. Bittensor, Akash,
Golem, Render, io.net, Gensyn and Morpheus all ship some subset of the five pillars today, and
Morpheus [21], [22] ships the specific combination the project claims as novel: Arbitrum L2
settlement plus provider bidding for LLM inference. The honest formulation, which is both defensible
and still a real contribution, is narrower: *no existing open-source system combines Kademlia-based
discovery, GossipSub second-price auctioning, an LLM-as-a-Judge verification pool with on-chain
slashing, and a Merkle-committed data-availability layer in one reproducible reference
implementation.* Lui and Sun [23] additionally provide the empirical finding that Bittensor's rewards
are driven overwhelmingly by stake rather than by output quality — a documented failure mode that
this project's verification-linked payment design can be positioned as a direct response to, which is
a far stronger argument than claiming no prior art exists.

**4.5 Scope divergences that the reference list must not disguise.** Consistency between the
references and the implementation is itself part of the honesty of the report. References [3] and [4]
should not be allowed to imply integrations that were not built. The report's scope table must state
plainly that Arbitrum Stylus (Rust/WASM) was **not** used — the contracts are plain Solidity 0.8.24
on a local Hardhat EVM chain — and that Celestia was **not** integrated; `edgegrid/da.py` is a local
namespaced blob store with real binary Merkle inclusion proofs, a documented stand-in behind the same
interface. References [3] and [4] therefore appear as **design rationale for a settlement and
data-availability architecture**, not as citations for deployed dependencies, and the surrounding
prose must say so.
