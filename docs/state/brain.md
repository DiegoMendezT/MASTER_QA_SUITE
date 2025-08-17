# Memory: Naming & Rules (authoritative)
- Canonical engine module: tools/task_prioritizer.py
- Legacy alias allowed ONLY via tools/innercouncil.py (shim). Do not remove.
- Config file: config/prioritizer_rules.yml
- Stability-first: do not rename core modules or configs.
- Before proposing refactors: run `python -m tools.consistency_check`.
