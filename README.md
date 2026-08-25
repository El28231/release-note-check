# Release Note Check

Maintains release-note versions, maps them to a numbered change manifest, and permits publication only when every required change is covered.

## Core workflow

- The owner stores a release name, numbered change manifest, explicit change count, coverage policy, and first notes draft.
- Validators return a binary coverage mask with one position per manifest entry.
- Any zero opens an owner-only revision path; an all-one mask opens the publish gate.
- Publishing records the exact accepted notes version.

## Reuse model

Deploy one instance per release. The instance supports up to six note versions without losing previous masks or drafts.

## Why GenLayer

Whether prose release notes accurately cover each material change is semantic. GenLayer creates the per-change mask through independent validator replay, while deterministic code verifies mask length and controls publication.

## Evidence and source boundary

The release name, numbered manifest, change count, coverage policy, and current notes version are the only evidence. No repository, changelog, or issue tracker is fetched.

## Safety boundary

Coverage is only as reliable as the supplied manifest and policy. The contract does not prove that the manifest is complete or that software behaves as described. The contract holds no funds, has no upgrade hook, and never treats a model result as real-world certification.

## Verify locally

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/release_note_check.py
genvm-lint typecheck contracts/release_note_check.py
pytest tests/direct -q
python tests/run_glsim.py --no-browser --seed 210821
gltest tests/integration/test_glsim_consensus.py -q --network localnet
```

Run the last two commands in separate terminals. Live StudioNet testing is opt-in and uses dedicated owner-specific keys outside this repository:

```text
gltest tests/integration/test_studionet_smoke.py -q -s --network studionet
```

Never commit a populated .env file, private key, keystore, or wallet password.

## Repository map

- contracts: deployable Intelligent Contract
- tests/direct: hardened state, authorization, malformed-output, and validator tests
- tests/integration: five-validator GLSim and live StudioNet flows
- deployments: public deployment and transaction evidence only
- SOURCE_POLICY.md: evidence authority and collection limits
- AUDIT.md: review-readiness checks and residual limitations
