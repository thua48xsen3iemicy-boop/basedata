---
name: review-unit
description: Independently review a proposed knowledge unit or assessment against evidence, declared outcomes, and local dependencies.
---

1. Read the scoped order, proposed diff, unit outcomes, source links and relevant prerequisites. Avoid opening unrelated tests or entire knowledge trees.
2. For each key claim record supported / unsupported / conflicted; assess depth, misleading wording, misconceptions and answer ambiguity.
3. Prefer independent, primary checks; an author LLM's claim is not a source.
4. Run deterministic validation where relevant; send findings with severity and file+ID references to `work/handoffs/<TASK-ID>/machine_reviewer.yaml`.
5. Recommend corrections or expert review. Never grant `expert_approved` / `published` status.
