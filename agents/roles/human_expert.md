# Role: human_expert

- **Executor:** qualified human.
- **Input:** one work order, scoped paths, relevant contracts, dependencies, evidence and previous role handoff.
- **Responsibility:** Review high-stakes facts, normative mappings and published content for correctness; explicitly accept risk.
- **Deliverable:** Recorded decision with name/role, timestamp, evidence and scope.
- **Boundary:** A model cannot impersonate this role or invent approval records.
- **Handoff:** Write `work/handoffs/<TASK-ID>/human_expert.yaml`: task ID, changed paths, sources/evidence, checks, unresolved findings, next role.
