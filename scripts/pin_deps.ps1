# scripts/pin_deps.ps1
# This script compiles all modular .in files into their corresponding .txt files.

Write-Host "Compiling all dependency files..."

$ErrorActionPreference = "Stop"

try {
    pip-compile requirements/base.in       -o requirements/base.txt
    pip-compile requirements/core-tests.in -o requirements/core-tests.txt
    pip-compile requirements/dev.in        -o requirements/dev.txt
    pip-compile requirements/ui.in         -o requirements/ui.txt
    pip-compile requirements/visual.in     -o requirements/visual.txt
    pip-compile requirements/data.in       -o requirements/data.txt
    
    Write-Host "✅ All requirement files pinned successfully."
}
catch {
    Write-Error "❌ Failed to pin dependencies. Please check the output above."
    exit 1
}
