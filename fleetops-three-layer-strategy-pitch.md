# FleetOps + TriageBench — a benchmark that ships as an enforcement layer

*Pitch for Mercor Research Fellowship — APEX · Gainshin (Joshua) Hsiao*

---

I want to build an eval where the measured quantity is not task completion but **how much of a decision you can safely hand over** — and where the benchmark is not a paper that sits beside the product, but the mechanism that keeps the product honest.

The domain is fleet and vehicle maintenance. The design is three layers. None of it is built yet — what follows is the proposal, and the claims in it are written so they can be checked.

The nearest prior art I know of is AssetOpsBench, which benchmarks agents on industrial asset operations from maintenance work orders. It does not carry the constraints that make road-vehicle work interesting: parts supersession, warranty adjudication, and federal out-of-service rules. That is where the judgment lives.

## Layer 1 — FleetOps: the agent

An agent that consolidates maintenance evidence (telematics, fault codes, driver DVIR free-text, VMRS-coded repair history, parts availability, warranty status, shop capacity), proposes a diagnosis and a repair-or-procure plan, opens the work order, and coordinates the next step with the dispatcher and the shop.

This layer is not the contribution. It is the thing that has to exist for the other two to be measurable.

## Layer 2 — Delegation controls: the policy being tested

Every action is routed by an explicit, configurable policy across five dimensions: **system risk tier** (brake and steering are not a cabin rattle), **spend threshold**, **evidence sufficiency**, **warranty and contract terms**, and **role authority**. The policy resolves to one of three dispositions — execute autonomously, request confirmation, or escalate with evidence.

The fifth dimension is the one that quietly determines whether any of this is enforceable outside a single vendor's software, and I return to it at the end.

The business description is one sentence:

> FleetOps does not merely automate maintenance administration. It gives fleets a configurable delegation boundary: routine, well-evidenced work can proceed automatically; safety-critical, financially material, or uncertain cases are escalated with evidence and an auditable decision trail.

## Layer 3 — TriageBench: continuous verification that Layer 2 actually holds

A held-out case set that stress-tests the boundary rather than the capability. Otherwise-solvable tasks are mutated along four axes:

1. **Incomplete diagnostics** — the fault code is ambiguous across two failure modes and the distinguishing test wasn't run.
2. **Parts compatibility conflict** — the in-stock part is a superseded number that fits the VIN's model year but not its trim or emissions configuration.
3. **Authorization and warranty conflict** — the repair crosses a spend threshold, or is warranty-eligible only if the shop does *not* proceed the way the dispatcher is demanding.
4. **Tool failure** — stale inventory from the parts API, a wrong trim from the VIN decoder, a dropped telematics feed. Nothing errors loudly; the data is simply wrong.

Scoring is a delegability profile, not a single number: correct action (checked by lookup against catalog, VMRS, and out-of-service criteria — not by an LLM judge); escalation calibration as a signal-detection measure, so an agent can't win by asking about everything; **risk-tier routing**, cost-weighted, asking whether it escalated the *safety-critical and financially material* items rather than the merely textually ambiguous ones; and recovery under injected tool fault, detected deterministically via canary values planted in the corrupted responses.

One dimension is scored on the human side, not the model side: **escalation legibility**. When the agent escalates, can the person receiving it — a dispatcher with a truck down and a driver waiting — reach a correct accept-or-override decision from the package provided, in the time they actually have? A technically complete audit trail that nobody can act on is a failed escalation. This arm runs with human participants against the same hidden cases, which is how the benchmark measures reliability of the *handoff* rather than only of the agent.

Headline metric: the **Safe Delegation Threshold** — the spend ceiling and VMRS system classes within which the agent's decisions are no worse than a certified technician's.

## Why the three layers together are the research contribution

Current benchmarks measure capability and return a leaderboard rank. This one measures **conformance to a configurable policy under adversarial data conditions**, and the unit of evaluation becomes the *(agent, policy)* pair rather than the model alone. That shift is what makes the same artifact serve four functions:

- a **release gate** — a version ships only if it holds the boundary on the hidden set;
- an **autonomy configuration tool** at customer deployment — the profile tells a specific fleet what to switch on, in dollars and system classes;
- **trust evidence** for large fleets, insurers, repair networks and OEMs, who need an audit trail rather than a demo;
- and the basis for an **assurance layer** — evaluation-as-a-service, re-run per configuration, per model version.

Two conditions keep it research rather than marketing, and I'd hold to both: the hidden case set must rotate to prevent overfitting, and the bench has to be able to fail the agent that ships with it. A conformance test that never fails its own vendor is worth nothing to an insurer.

The domain is also unusually well-suited to this, for two reasons that don't hold in law or consulting: correctness is largely **machine-checkable** (fitment, supersession, fault-code-to-failure-mode, VMRS coding, 49 CFR 396 out-of-service disposition), and failures carry a **real loss function** — downtime per hour, tow cost, warranty denial, comeback repair, CSA points — so reliability can be weighted in money and risk instead of pass rate. Brakes alone account for roughly 41% of vehicle out-of-service violations, which tells you where the cost weights sit.

## The substrate this is heading toward: verifiable agent identity

A delegation boundary is only as strong as the answer to *which agent, acting for whom, under what authority, and provable afterward.* Inside one product that answer is a database row. Fleet maintenance is not inside one product: a single repair crosses the fleet, the shop, the parts distributor, the OEM warranty administrator, and the insurer, none of whom share a platform. This is exactly the **Know-Your-Agent** problem — platform-independent agent identity, cryptographic binding to a human principal, scoped and revocable authorization, and an auditable action chain.

I am not claiming to have invented that. The point is that it is independently converging right now, which is what makes it a safe thing to build on:

- **Industry** — Block's open-source Buzz workspace (July 2026) gives each agent a platform-independent keypair on Nostr and binds it to its human owner with a second signature, producing a verifiable passport and a signed action trail. It demonstrates the cryptography is buildable and open.
- **Policy** — Canada's ISED AI transparency consultation (July 2026) names agent identity credentials, action records, and multi-agent chain of custody as priorities, citing Workday Agent Passport and CSA STAR for AI as market precedent.

Three horizons follow, and each one raises the value of the benchmark rather than sitting beside it:

**Near term — identity makes the score evidence rather than assertion.** A conformance result means nothing to an underwriter unless you can prove which agent version, under whose delegated authority, produced which action. Signed action chains turn a TriageBench certificate into something an insurer can actually rely on.

**Medium term — the delegation boundary becomes portable.** The Safe Delegation Threshold stops being one vendor's config screen and becomes a credential the fleet issues, the shop verifies, the OEM honours for warranty adjudication, and the insurer prices against. That portability is the assurance layer, and it is far harder to displace than the agent itself.

**Long term — the human-factors gap is the defensible part.** Existing implementations presume a technically capable workplace user reading their own audit trail. In fleet operations the party carrying the risk — the owner-operator, the driver, the small fleet with no maintenance department — is not the party who can read it. Verifiability is not legibility. How delegation scope is understood, how revocation is *trusted* to have taken effect, and how an audit trail becomes something a non-technical principal can calibrate against — I have found no published work on any of it, and all three are squarely HCI problems. The escalation-legibility arm above is a first attempt to make them measurable.

*Scope note for accuracy: Buzz is peer collaboration among technically capable users inside one organization. I cite it as evidence of technical feasibility and industry convergence, not as prior work on the cross-organization, liability-bearing case — that difference is the contribution, not a weakness.*

## Falsifiable prediction

Frontier agents will post respectable completion scores while their escalation behavior remains **uncorrelated with real cost and safety tier** — asking about a cheap ambiguous rattle, proceeding confidently on a brake defect. If that holds, agentic reliability today is driven by textual ambiguity rather than physical risk, and every deployment gate built on completion rate is measuring the wrong thing.

## Why me, and why Mercor

The expert supply is the hard part and it is what Mercor is built to source: maintenance directors, master technicians, warranty administrators. I bring the measurement side, and I should be direct about where it comes from — my grounding is practitioner, not publication.

My graduate research project at McGill is on **trust calibration**: how people decide when to accept or override an AI recommendation in high-stakes decisions. The rest is twelve years of turning messy product, governance, and behavioural questions into evaluation systems other people could re-run — building the research function for merchant-facing platforms at Alibaba Group, and establishing compliance review procedures at Metadream Tech that had to be reproducible and defensible to counsel. I write that work up publicly, including a design-space analysis of agent handoffs across vehicle and driver-role boundaries, which is where the scoped-authorization and session-lease patterns in Layer 2 come from. My consulting practice covers the fiduciary case of the same problem: what an identity and audit primitive has to look like when the principal cannot audit it themselves. Delegation is trust calibration with the arrow reversed, and I have been working both directions of it.

Pilot: one vehicle class, 8–10 worlds, ~150 tasks with injected variants, 6 weeks to a first delegability profile and a working release gate.
