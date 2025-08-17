#!/bin/bash
# scripts/pin_deps.sh
# This script compiles all modular .in files into their corresponding .txt files.

echo "Compiling all dependency files..."

pip-compile requirements/base.in       -o requirements/base.txt && \
pip-compile requirements/core-tests.in -o requirements/core-tests.txt && \
pip-compile requirements/dev.in        -o requirements/dev.txt && \
pip-compile requirements/ui.in         -o requirements/ui.txt && \
pip-compile requirements/visual.in     -o requirements/visual.txt && \
pip-compile requirements/data.in       -o requirements/data.txt

if [ $? -eq 0 ]; then
    echo "✅ All requirement files pinned successfully."
else
    echo "❌ Failed to pin dependencies."
    exit 1
fi
