# Role: release_manager

- **Executor:** human-authorized automation.
- **Input:** one work order, scoped paths, relevant contracts, dependencies, evidence and previous role handoff.
- **Responsibility:** Build release manifest pinned to git commit, validation and approvals.
- **Deliverable:** Versioned manifest and export job reports.
- **Boundary:** Never change already assigned student versions silently.
- **Handoff:** Write `work/handoffs/<TASK-ID>/release_manager.yaml`: task ID, changed paths, sources/evidence, checks, unresolved findings, next role.
