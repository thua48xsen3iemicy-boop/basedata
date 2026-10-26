---
name: draft-unit
description: Draft one atomic learning unit from a bounded work order with primary sources, misconceptions, and measurable outcomes.
---

1. Read root `AGENTS.md`, assigned `work/orders/<TASK-ID>/order.yaml`, nearest scoped `AGENTS.md`, and `contracts/CONVENTIONS.md`.
2. Search existing unit IDs first. Stop if an equivalent outcome already exists; propose a reuse mapping instead of cloning text.
3. Work **only** inside allowed paths. Research versioned primary sources; track disputed statements explicitly.
4. Create/update `unit.yaml`, `canonical.md`, `sources.yaml`, and `misconceptions.yaml`, keeping canonical text compact and precise.
5. Run `python tools/validate.py`. Store concise handoff in `work/handoffs/<TASK-ID>/author.yaml`.
6. Leave status `draft`. Hand to machine reviewer; do not approve or publish.
