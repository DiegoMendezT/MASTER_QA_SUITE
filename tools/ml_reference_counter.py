# ML Reference Count Automation Script

# This script will recursively scan all files in the project for 'ML' and 'ML-Enabled' (case-insensitive, including variations),
# log each file's count and running total to 'artifacts/ml_reference_count_log.md', and output the final total.
# Excludes files/folders in .gitignore and common binary types.

import os
import re
from pathlib import Path

# Patterns to match
patterns = [re.compile(r'\bml(-enabled)?\b', re.IGNORECASE)]

# Exclude patterns (from .gitignore and common binary types)
EXCLUDE_DIRS = {'.git', '.venv', 'venv', 'env', '__pycache__', 'build', 'dist', 'downloads', 'eggs', '.eggs', 'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels', '.egg-info', 'develop-eggs', 'MANIFEST', '.Python', 'wheels', 'sdist', 'eggs', 'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels', 'downloads', 'eggs', '.eggs', 'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels', 'downloads', 'eggs', '.eggs', 'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels'}
EXCLUDE_FILES = {'.DS_Store', 'Thumbs.db'}
EXCLUDE_EXTS = {'.pyc', '.pyo', '.so', '.egg', '.manifest', '.spec'}

# Log file
log_path = Path('artifacts/ml_reference_count_log.md')
log_path.parent.mkdir(exist_ok=True)

running_total = 0
with open(log_path, 'a', encoding='utf-8') as log:
    for root, dirs, files in os.walk('.'):
        # Exclude dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file in EXCLUDE_FILES or any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                continue
            file_path = Path(root) / file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                count = sum(len(p.findall(content)) for p in patterns)
                if count > 0:
                    running_total += count
                    log.write(f"{file_path}: {count} (Running total: {running_total})\n")
            except Exception as e:
                log.write(f"{file_path}: ERROR ({e})\n")
    log.write(f"\nFINAL TOTAL: {running_total}\n")
print(f"ML reference count complete. Final total: {running_total}")
