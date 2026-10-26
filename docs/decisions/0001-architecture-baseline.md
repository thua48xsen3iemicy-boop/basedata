# ADR-0001: Repo-first architecture baseline (provisional)

Status: **proposed**. Date: 2026-10-26. Owners: to be appointed.

## Decision

Use one Git repository for human-readable content, source provenance, contracts, machine-checkable references and work orders. Write a small deterministic validator and CI. Keep a single stable knowledge ID independent of course/formulation. Separate requirement versions and pedagogical routes. Human publication decisions need future audited gate; until then drafts only.

## Why

We need cheap parallel contributions by small LLMs; local scope, file diffs and PR review are easier to audit than a shared mutable chat. The initial content is sufficiently small for files+Git; runtime indexing/search can be derived later.

## Tradeoffs / alternatives

- **Database-first:** more expressive relational constraints/search; premature ops/synchronization overhead for authoring now. Keep possible generated indexes, migrate if measured need.
- **One large curriculum per profession:** initially simpler but guarantees content duplication and source drift; rejected.
- **Fully autonomous publish:** high risk of plausible inaccuracies, answer-key errors, regulatory mismatch; rejected.
- **One universal AI prompt:** bloats context and causes inconsistent local responsibilities; rejected for root AGENTS + scoped tasks + targeted skills.

## Revisit triggers

Growth in IDs/merge conflicts, validator performance, unavoidable multi-writer edits, normative mapping complexity, release/approval requirements, deployment consumers.
