# Architecture

## Responsibility boundary

The application may collect inputs and display state. ReleaseNoteCheck owns the bounded on-chain record, authorization rules, semantic consensus call, and consequential state transition. There is no hidden backend or autonomous source collector.

## State machine

DRAFT -> GAPS_FOUND -> DRAFT, or DRAFT -> PUBLISHABLE -> PUBLISHED.

## Storage model

The contract stores owner, release metadata, manifest and count, policy, note versions, per-version binary masks, phase, audit count, and published version. Text is normalized and field-length-bounded before storage.

## Consensus boundary

The leader serializes only stored case data into canonical JSON and requests an exact JSON schema. Validators independently run the same prompt and normalization path. A validator accepts only an allowed, structurally valid value that exactly matches its own result. Exceptions and malformed output fail closed.

## Authorization and invariants

Consensus audit is permissionless. Only the owner may submit a requested revision or publish an all-covered version.

## Reuse and distinctness

Deploy one instance per release. The instance supports up to six note versions without losing previous masks or drafts.

This is a positional coverage ledger and deterministic publish gate, not a single COMPLETE/PARTIAL label or a best-note tournament.
