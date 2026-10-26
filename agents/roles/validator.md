# Role: validator

- **Executor:** code / deterministic.
- **Input:** one work order, scoped paths, relevant contracts, dependencies, evidence and previous role handoff.
- **Responsibility:** Check schemas, referential integrity, totals and state/permission constraints; report failures.
- **Deliverable:** CI report with file-path IDs and failure reasons.
- **Boundary:** Passing CI never proves factual accuracy.
- **Handoff:** Write `work/handoffs/<TASK-ID>/validator.yaml`: task ID, changed paths, sources/evidence, checks, unresolved findings, next role.
