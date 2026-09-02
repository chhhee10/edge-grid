# Chapter 9

# CONCLUSION AND FUTURE WORK

## 9.1 Conclusion

This project set out to determine whether the five mechanisms that the literature of decentralised
machine learning studies separately — peer-to-peer discovery, a market protocol for scheduling,
an edge inference runtime, verifiable output commitments, and blockchain settlement with staked
collateral — can be composed into a single job pipeline that runs end to end, and whether that
composite can be measured rather than merely described. The answer established by Chapter 8 is
that it can. A request published to a GossipSub task mempool is auctioned under a sealed-bid
second-price rule among real provider processes, executed by a streaming open-weight runtime on
commodity hardware, committed as a namespaced blob whose Merkle root is posted on chain,
sampled for audit by a keyed hash of the job identifier, judged against a five-point rubric by a
validator that returns pass, fail or error, and finally settled or slashed by a Solidity escrow
contract whose state machine rejects every illegal transition. Every stage of that sentence
corresponds to code that was executed, and the latency, auction, verification, settlement and cost
stages each have a timestamped run directory under `docs/results/` carrying its own configuration
snapshot and commit hash. Two clauses rest on a different kind of evidence and are named as such:
the audit sampler ran at a rate of one in the measurement harness, since the harness exists to
measure the judge rather than the sampler, and the escrow contract's rejection of every illegal
transition is established by the contract test suite rather than by a run.
The claim of this work is therefore integration and
empirical characterisation, exactly as bounded in Section 6.5, and that claim is supported.

Three results carry the claim. The first is latency. On a Tier 1 CPU node with sixteen logical cores,
approximately thirty-one gigabytes of memory and no accelerator, warm time-to-first-token was
measured at a mean of 609.6 ms, a median of 587.9 ms and a 95th percentile of 723.6 ms over twenty
trials, with a standard deviation of 75.7 ms; twenty of the twenty warm trials fell below one second,
so Objective 7's sub-second target is met on this hardware. The figure is reported beside its cold
counterpart, as the protocol of Chapter 3 requires: over five matched evict-and-reload pairs, cold
TTFT averaged 7,963.8 ms against a paired warm mean of 653.7 ms, a ratio of 12.18 and an absolute
penalty of 7,310 ms. Model residency, and not generation, dominates the latency budget of an edge
node, which is the empirical justification for the warm-start bonus carried in the auction score.
Sustained throughput on the same node was 12.86 tokens per second. These are shown in
Figure 8.1 (`docs/figures/fig_ttft.png`).

The second result is the market. The auction was exercised over a real py-libp2p GossipSub mesh
between separate operating-system processes at three, four and five nodes, nineteen auctions at each
size, fifty-seven in total. The first bid reached the requester in 16.9 ms, 22.3 ms and
21.1 ms respectively, and the last bid in 21.3 ms, 32.6 ms and 36.7 ms, so bid dispersion grows
modestly with node count while remaining between one and two orders of magnitude below the
clearing interval.
Broadcast-to-award was 2,007 to 2,008 ms at every node count, because it is pinned by the fixed
two-second bid window and is therefore a constant of the configuration rather than a scaling
measurement; the bid arrival times are the signal, and the award figure is not. Mesh formation took
7.9 to 8.2 seconds. Figure 8.2 (`docs/figures/fig_auction.png`) presents both quantities together so
that the constant is not mistaken for a result.

The third result is settlement. Four contracts were compiled and deployed to a local EVM chain of
chain identifier 31337 at a total deployment cost of 4,831,798 gas, and a complete job lifecycle was
driven down each of the three resolution paths the design admits. All three resolved correctly: an
honest job whose challenge window elapsed reached the settled state; a job for which a data
mismatch was proved against the committed hash was slashed; and a job that a validator returned a
failing verdict on was slashed. The eighty-twenty slash distribution was verified on chain, with
0.04 GRID credited to the detecting validator and 0.01 GRID to the treasury out of a 0.05 GRID
slash, and value conservation was checked against on-chain balances rather than against the
simulation's own bookkeeping. Gas per operation ranged from 32,317 for a withdrawal to 221,353
for `proveDataMismatch`, as set out in Figure 8.6 (`docs/figures/fig_gas.png`). The cost model
places the grid at \$0.001151 per thousand delivered tokens — \$0.001096 of inference and
\$0.000055 of amortised verification — against a \$0.002000 centralised baseline, a ratio of 0.576,
with verification accounting for 4.76 per cent of grid cost at the five per cent audit rate. Because
GRID has no market price, that dollar comparison is a cost model at a stated notional rate and not a
market observation; the GRID-denominated and gas-denominated figures are the measurements.
The implementation is exercised by 346 pytest tests and 39 Hardhat tests, all of which pass.

One result qualifies the claim, and it is the most consequential finding of the project. The judge
achieved 100 per cent precision with a false-positive rate of zero — not one of the twenty honest
answers was failed — but its recall was 65 per cent, and that recall is not uniform across the four
injected fraud strategies. It caught 100 per cent of off-topic substitutions and 95 per cent of
hallucinated entities, but only 35 per cent of incorrect-answer substitutions and 30 per cent of
negations. The mean-score column establishes that this is not hesitation near the threshold: missed
frauds scored 3.80 and 4.05 on average against a pass threshold of 3, so the judge was confidently
endorsing them. It scored the TruthfulQA-labelled misconception "Einstein flunked math in school"
at 4 out of 5, and "Marie Antoinette actually said, 'Let them eat cake'", "Sigmund Freud said,
'Sometimes a cigar is just a cigar'" and "Agenda 21 is not a United Nations action plan on
sustainable development" at 5 out of 5 each. On several negations its written justification asserted
the opposite of the sentence it had just read. The interpretation this report advances, and which
Figures 8.3 and 8.4 (`docs/figures/fig_verification.png`, `docs/figures/fig_score_dist.png`) support,
is that a judge drawn from the same model family as the provider inherits that family's errors and
cannot police a misconception that it also holds. This bears directly on how the earlier
false-positive problem should be understood. The Phase-1 run reported 83.87 per cent precision and
97.5 per cent recall while failing fifteen of twenty honest answers, a 75 per cent false-positive rate;
the present run reports 100 per cent precision and zero false positives with nothing whatever
changed about the judge. What changed is the source of the honest answers, which are now
generated by the real local node rather than by a weak hosted model whose outputs were frequently
wrong on their own merits, and which the judge was therefore often right to fail. The false-positive
problem was a generator problem misdiagnosed as a judge problem, and correcting the diagnosis
exposed the real weakness underneath it.

## 9.2 Contributions

The contributions of this work are stated below in bounded form. Section 6.4 lists in detail what
this project does not claim to have invented, and that list is not repeated here; it is sufficient to
restate that no individual mechanism used in the system is offered as novel. Kademlia routing,
GossipSub, the Vickrey auction, quantised inference on consumer hardware, the LLM-as-a-Judge
paradigm, optimistic fraud proving, data-availability sampling and staked settlement are all prior
art, and this project consumes each of them as such.

**1. A composed and runnable reference implementation.** Discovery over py-libp2p, a GossipSub
sealed-bid second-price auction, a streaming open inference runtime, a namespaced Merkle-committed
data-availability store with checkable inclusion proofs, a sampled judge with three-valued verdicts,
and staked Solidity settlement with an escrow state machine are wired into one pipeline in which a
single job travels the whole distance. The contribution is the composition as an artefact, not any
layer within it, and it is bounded by the substitutions declared in Section 7.8: the data-availability
layer is a local stand-in for Celestia, the contracts are plain Solidity rather than Arbitrum Stylus,
and the runtime is CPU-bound Ollama rather than vLLM on CUDA.

**2. End-to-end measurement of the composite under a declared protocol.** The quantities reported
in Chapter 8 are properties of the assembled pipeline rather than of any one layer — the dominance
of the cold-start penalty over the latency budget and its consequence for auction design, judge
precision and recall against systematically injected fraud, the share of delivered-token cost
consumed by verification itself, gas per settlement operation, and conservation of value across
escrow, payout and slashing. Each is recorded in its own run directory with a configuration
snapshot and a commit hash, so that any figure in this report can be traced to the execution that
produced it. This contribution is bounded by scale: one machine, small N, and a local chain.

**3. The finding that a same-family judge inherits the errors it is deployed to police.** This is the
substantive empirical contribution. Detection is high where fraud is lexically conspicuous and
collapses where fraud is semantically subtle, and the mean-score evidence shows the failures to be
confident rather than marginal. The finding is bounded in the obvious ways — one judge model of
approximately two billion parameters, twenty questions, four synthetic corruption strategies — but
the mechanism it identifies is not an artefact of those bounds, since a judge cannot be expected to
reject a proposition it independently believes.

**4. The observation that economic security is bounded by the judge's worst strategy, not its
average.** A rational adversary does not sample uniformly from the strategy space; it selects the
strategy that evades detection. The security-relevant figure for this configuration is therefore
30 per cent, the recall against semantic negation, and not the 65 per cent overall. Stating the
average alone would overstate the deterrent by more than a factor of two. This observation is an
argument about how such systems must be evaluated rather than a new mechanism, and it is offered
as such.

**5. Empirical support for two design decisions the architecture already contained.** The
verification result is a direct argument for the validator *pool* with a quorum and deliberate model
diversity, rather than the single judge that the recorded runs used, because correlated judges
inherit correlated blind spots and adding more of the same model would not help. It also raises the
relative value of the trustless data-mismatch fraud proof, which establishes that a provider served
something other than what it committed to, requires no model and no judgement of quality at all,
and cost 221,353 gas in the measured run. Where the judge is fallible, that path is not.

**6. A measurement of judge instability under paraphrase.** Restating the same claim in different
words changed the judge's verdict on two of eight answers, a twenty-five per cent flip rate, with
individual answers scoring 1 and 5 on the same claim in the same run. Both flips fell on questions
turning on a quantifier — the same semantic territory in which negation defeated detection — so two
independent instruments locate the failure in the same place. The consequence is sharper than
inaccuracy: a slashing rule built on a single verdict is arbitrary at the margin, and a rational
provider prices the risk of being slashed for correct work into its bid, so the cost is paid by
honest participants. The measurement is bounded by a small sample and by the use of the judging
model as its own paraphraser, and both bounds would more plausibly raise the rate than lower it.

**7. A declared-scope methodology.** Every substitution of a locally runnable component for a
hosted one is stated in Table 1.1 and Section 7.8, implemented behind the interface of the
component it replaces, and paired with the migration path back. This is a small contribution but a
real one, in that it makes the artefact's limitations checkable rather than requiring the reader to
accept the report's account of its own capabilities.

## 9.3 Limitations

The limitations set out at length in Section 8.7 are condensed here without softening.

The judge is a local model of approximately two billion parameters. A larger or better-aligned judge
would very likely score higher on the strategies where this one failed, so the 30 per cent figure
should be read as a property of this configuration and not as a bound on the design. It is, however,
the figure that would have governed economic security had this configuration been deployed.

The negation templates used by the fraud injector are stilted in ways that a genuine adversary
would avoid. Several begin with a formulaic clause of the form "Contrary to popular belief, it is
completely false that", which a competent attacker would never emit. This cuts in both directions:
it may have made some frauds easier to detect than they would be in the wild, and it certainly does
not establish that the judge would perform better against fluent adversarial paraphrase.

The verification result rests on twenty questions in five conditions on a single machine, a hundred
judged trials in total. The judge self-consistency check recorded in Table 8.4 is smaller again —
eight answers and thirty judgements — and at that size the twenty-five per cent verdict flip rate
it reports should be read as evidence that the instability is real and material, not as a precise
estimate of its magnitude. The paraphrases were moreover generated by the same model that judged
them, which is the design most likely to produce paraphrases the judge finds easy; an independent
paraphraser would be a stronger test, and would be at least as likely to raise the measured rate
as to lower it.

The system is not deployed. The auction experiment runs separate operating-system processes on
one host, which measures protocol and scheduler overhead and not wide-area latency, network address
translation, packet loss or peer churn; a five-process run on one machine is not a five-machine
deployment and is not described as one anywhere in this report. The chain is a local EVM chain,
which yields real gas semantics and real measured gas but no fee market and no finality under
contention. The data-availability layer is a local Merkle-committed store providing the binding
property that the fraud proof consumes, but not Celestia's availability guarantee under a
decentralised validator set. There is no NVIDIA GPU on the development hardware, so all inference
figures characterise the CPU tier only. The stakes are test values, so no conclusion follows about
the adequacy of any particular stake level or slash share as a deterrent, because no participant in
these runs had anything to lose. Finally, the dollar figures in the cost comparison are a model at a
stated notional rate for a token that has no market price.

## 9.4 Future Work

The ordering below follows what the measured results actually motivate.

**1. A diverse validator pool with quorum.** This is the first priority because the verification
result identifies the specific mechanism by which a single judge fails. The `ValidatorPool`
abstraction and the quorum tally already exist in the implementation and were exercised with a pool
size of one; the work is to populate the pool with judges drawn from *different* model families and
to measure whether the strategies that defeated the present judge — negation and incorrect-answer
substitution — are caught by a model that does not share its priors. The hypothesis to test is that
detection improves with model diversity rather than with pool size, and it is falsifiable: a pool of
several instances of the same model should show little improvement, which would confirm the
inheritance mechanism, whereas a mixed pool should show a marked one. The tally rule, which
checks `fail` before `pass`, and the quorum threshold both need re-examination once votes are no
longer correlated by construction.

**2. A multi-machine deployment on a local area network.** This converts the largest single threat
to validity into a measurement. Running three to five nodes on physically distinct hosts would
subject the discovery layer, the GossipSub mesh and the bid window to real network delay, clock
skew and peer churn, and would establish whether the two-second bid window is adequate or merely
convenient. It would also permit the first honest test of the geographic-proximity argument on
which the latency case for edge inference partly rests, which the present single-host measurements
cannot address at all.

**3. A larger or fine-tuned judge.** A judge with substantially more parameters, or one fine-tuned
on TruthfulQA and preference data as the original synopsis proposed, should be evaluated against
the same hundred-trial protocol so that the results are directly comparable. This is placed third
rather than first deliberately: the evidence gathered here suggests that model *diversity* may
matter more than model *size*, because a larger model from the same family may simply hold the
same misconceptions more confidently. The two variables should be separated in any such study
rather than confounded. The paraphrase self-consistency check should be repeated at a larger
sample and with an independent paraphraser, since a twenty-five per cent flip rate measured over
eight answers is enough to establish that the problem exists and not enough to size it.

**4. The production substitutions.** Three components should be replaced with the systems named in
the original design. The data-availability layer should be migrated to a Celestia light node, which
requires reimplementing `submit_blob()` and `get_blob()` and nothing else, and which would supply
the availability guarantee that the local store cannot. The contracts should be deployed to an
Arbitrum testnet, which would subject the same EVM semantics to a real fee market and real
finality, and which is the precondition for any later Stylus port. A CUDA path through vLLM should
be added behind the existing `run()` entry point and benchmarked on Tier 3 hardware, so that the
serving economics of the discrete-GPU tier the network intends to recruit can be characterised
rather than assumed. Alongside these, content-addressed model-weight distribution over IPFS
remains unimplemented, although the on-chain binding from model identifier to weight hash that
makes it auditable is already present in `ModelRegistry`.

**5. Zero-knowledge machine learning.** The design adopts a two-tier verification philosophy of
which only the optimistic tier is built. Replacing the judge with a succinct cryptographic proof
that a specified model was executed on a specified input would eliminate the entire class of failure
documented in this chapter, because a proof system does not hold opinions about Marie Antoinette.
It is placed last because the cost is presently prohibitive: proving transformer inference remains
several orders of magnitude more expensive than the inference itself, which is irreconcilable with a
sub-second time-to-first-token target. The honest framing is that this is a direction the
architecture is compatible with — the fraud-proof interface would accept a validity proof in place
of a mismatch proof with modest change — and not a plan that present techniques can execute for
real-time inference.

## 9.5 Closing Remarks

The Edge Grid, as submitted, is a working composition of five mechanisms that the literature has
studied in isolation, measured end to end under a protocol that records where every number came
from. Its strongest result is that the pipeline holds together: sub-second warm inference, a market
that clears over a real gossip mesh, and settlement that resolves correctly down all three of its
paths. Its most useful result is the one that went against expectation, namely that the judge on
which the economic security of the whole arrangement rests is confidently wrong about precisely the
frauds an adversary would choose, and that the fault lies not in the judge's calibration but in its
kinship with the model it is asked to police. That finding is a reason to build the validator pool
with diversity as a design requirement rather than an optimisation, and it is offered here as a
measured constraint on the design rather than as a defect of it.
