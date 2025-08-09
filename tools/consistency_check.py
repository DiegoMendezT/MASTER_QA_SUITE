import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

must_exist = [
  "tools/task_prioritizer.py",
  "config/prioritizer_rules.yml",
]
legacy_tokens = [
  "innercouncil.rules.yml",  # legacy filename
]

# Check files exist
missing = [m for m in must_exist if not (ROOT / m).exists()]
if missing:
    print("[FAIL] Missing required files:")
    for m in missing: print(" -", m)
    sys.exit(1)

# Scan for legacy tokens
bad = []
my_path = str(pathlib.Path(__file__).relative_to(ROOT))
for p in ROOT.rglob("*"):
    if str(p.relative_to(ROOT)) == my_path:
        continue
    if p.is_file() and p.suffix in {".py", ".yml", ".yaml", ".md"}:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if any(tok in txt for tok in legacy_tokens):
            bad.append(str(p.relative_to(ROOT)))

if bad:
    print("[FAIL] Legacy references detected:")
    for b in bad: print(" -", b)
    sys.exit(1)

print("[OK] naming consistency")
