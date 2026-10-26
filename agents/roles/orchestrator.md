# Role: orchestrator

- **Executor:** strong / planner.
- **Input:** one work order, scoped paths, relevant contracts, dependencies, evidence and previous role handoff.
- **Responsibility:** Map competencies, prioritize gaps, split work into bounded independent work orders.
- **Deliverable:** Work order with goals, allowed paths, prerequisites, quality gates and reviewer assignment.
- **Boundary:** Do not author a giant course or alter standards while planning.
- **Handoff:** Write `work/handoffs/<TASK-ID>/orchestrator.yaml`: task ID, changed paths, sources/evidence, checks, unresolved findings, next role.
