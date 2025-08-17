# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: RELEASE_PROCESS.md
# Purpose: Defines the release process and tagging policy for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# Release Process

**Date:** 2025-08-10 13:45 UTC

## House Rule

No merge to `main` without a release tag. Every merged PR must result in either:

- A patch/minor release tag (`vX.Y.Z`), or
- A release candidate tag (`vX.Y.Z-rc.N`) that promotes to release within 24 hours.

This keeps history traceable and rollbacks trivial.

## Commands for Releases

### Create a Release Tag
```bash
# Example for v1.0.1
git add -A
git commit -m "chore(release): prep v1.0.1 — freeze, docs, CI guardrails"
git push origin main
git tag -a v1.0.1 -m "v1.0.1 — stability release (visual on standby)"
git push origin v1.0.1
```

### Rollback Playbook
```bash
# Example for reverting v1.0.1 to v1.0.0
git checkout main
git pull
git checkout -b revert/v1.0.1-to-v1.0.0
git reset --hard v1.0.0
git push -u origin revert/v1.0.1-to-v1.0.0
# Merge PR, then:
git tag -a v1.0.2 -m "revert to v1.0.0"
git push origin v1.0.2
```

## CI/CD Guardrails

### Workflow Configuration
Add the following to `.github/workflows/tests.yml`:
```yaml
name: tests
on:
  push: { branches: [main], tags: ['v*.*.*'] }
  pull_request: { branches: [main] }

jobs:
  qa:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        engine: [selenium, playwright]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('dependencies.txt') }}
      - name: Install deps (locked)
        run: pip install -r dependencies.txt
      - name: Install Playwright browsers
        run: python -m playwright install --with-deps chromium firefox webkit
      - name: Consistency gate
        run: python -m tools.consistency_check
      - name: Run tests (non-visual)
        run: python -m pytest -n auto -m "not visual" --engine=${{ matrix.engine }} -q
      - name: Upload pytest report
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: pytest-${{ matrix.engine }}, path: reports/report.html }

  release:
    if: startsWith(github.ref, 'refs/tags/v')
    needs: [qa]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate release notes
        id: notes
        uses: actions/github-script@v7
        with:
          script: |
            core.setOutput("body", "Automated release for " + context.ref)
      - name: Publish GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.notes.outputs.body }}
          files: |
            reports/**/*.html
```
