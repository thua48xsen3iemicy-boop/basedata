# Orders and handoffs

Every contributor works from one isolated `work/orders/<TASK-ID>/order.yaml`; assign unique IDs (issue number or UUID) to prevent collisions. The task defines allowed paths, acceptance, assigned role and scoped input IDs. Handoff is written to `work/handoffs/<TASK-ID>/<role>.yaml` and is append-by-role, not a mutable central transcript. Keep handoffs compact: next agent should not need a full chat history.

A public issue can be converted into a work order using `ORDER_TEMPLATE.yaml`. Work order names in this starter are examples and contain no real issue assignment.

**Структурный handoff:** `contracts/handoff.schema.json`. Путь содержит тот же task ID, имя файла — имя роли: `work/handoffs/TASK-DEMO-001/author.yaml`. В `changed_paths` указываются только содержательные изменённые пути в `scope.allowed_paths`, не сам handoff. Проверяет `tools/validate.py`. Опциональные поля заказа: `model_tier` и `depends_on` (по существующим task IDs).

Модель получает только `order.yaml`, ближайший `AGENTS.md`, нужные ID и предыдущие артефакты. Если задача большая, нарежьте несколько уникальных заказов; не поручайте нескольким моделям один `canonical.md`.
