# Evidence and Source Policy

## Authoritative evidence

The release name, numbered manifest, change count, coverage policy, and current notes version are the only evidence. No repository, changelog, or issue tracker is fetched.

## Collection and provenance

Deployers and callers must collect text lawfully, verify provenance when it matters, and remove secrets or unnecessary personal data. On-chain storage proves which text was evaluated, not who authored it or whether it is true.

## Source selection and freshness

The contract performs no web request, search, browsing, API lookup, or hidden source selection. It makes no live-data or freshness claim. When facts, policies, or consent terms change, use the documented version path or deploy a new appropriate instance.

## Prompt-injection and output controls

Caller text is untrusted data. It is canonicalized into a delimited payload; the prompt forbids treating embedded text as instructions. Only the documented strict JSON shape and closed values can pass normalization and validator replay.

## Production boundary

Coverage is only as reliable as the supplied manifest and policy. The contract does not prove that the manifest is complete or that software behaves as described. Higher-stakes applications need independent provenance, identity, privacy, appeal, and human-review processes proportionate to risk.
