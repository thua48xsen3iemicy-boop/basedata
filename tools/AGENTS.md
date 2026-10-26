# Validator/tool code

Tests are required for changes to validation behavior. Prefer deterministic, local operations. Do not add network calls or expensive model queries to mandatory CI. Model-based QA is a separate optional gate. Keep error messages path-specific and actionable.
