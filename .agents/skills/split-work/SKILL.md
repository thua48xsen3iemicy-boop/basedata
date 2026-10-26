---
name: split-work
description: Turn a large course or knowledge-gap request into small non-conflicting agent work orders with explicit acceptance criteria.
---

1. Read `docs/PROJECT_BRIEF.md`, `docs/ARCHITECTURE.md`, `docs/AGENT_WORKFLOW.md` and existing ID/path inventory for the requested domain only.
2. Identify stable facts, assessable outcomes, missing prerequisite units and sources; avoid generating a course-length narrative.
3. Create separate `work/orders/<TASK-ID>/order.yaml` files from the template, one owner/role/path scope per order.
4. Mark cross-directory changes as separate dependency tasks. Never allocate two simultaneous authors to the same canonical file.
5. Recommend assignment order: research → content draft → questions → independent review → deterministic checks → human approval.
