# JIRA Integration Guide

## Project Basics
- **Key:** MQS
- **Components:** Core, CI, Docs, Playwright, Selenium, Streamlit, Client-Baseline
- **Labels:** kintsugi, innercouncil, hotfix, smoke, regression

## Issue Types & Fields
- **Types:** Bug, Task, Hotfix, Spike
- **Custom Fields (optional):**
  - Voice (single-select: Architect, Engineer, Gatekeeper, ReleaseCaptain, Copilot)
  - Engine (multi-select: Selenium, Playwright)
  - Risk (Low/Med/High)

## GitHub Integration
- In Jira: Projects → Project settings → Integrations → GitHub (or “DVCS accounts”) → connect repo.
- In GitHub: add secrets for automations:
  - JIRA_BASE_URL (e.g., https://masterqasuite.atlassian.net)
  - JIRA_USER_EMAIL
  - JIRA_API_TOKEN (from Atlassian account)

## CI Failure → Jira Issue (freeze-safe)
Append to `.github/workflows/tests.yml`:
```yaml
  jira:
    name: jira (file on failure)
    needs: [tests]
    if: ${{ failure() && secrets.JIRA_API_TOKEN != '' }}
    runs-on: ubuntu-latest
    steps:
      - name: Create Jira issue on failure
        env:
          JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
          JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_PROJECT_KEY: MQS
          RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
        run: |
          TITLE="CI failed on ${{ github.ref_name }} — ${{ github.workflow }}"
          BODY="CI run: ${RUN_URL}\nCommit: ${{ github.sha }}\nEngine/Browser matrix may contain failing legs.\nArtifacts: reports/, screenshots/."
          curl -s -X POST \
            -H "Content-Type: application/json" \
            -u "${JIRA_USER_EMAIL}:${JIRA_API_TOKEN}" \
            "${JIRA_BASE_URL}/rest/api/3/issue" \
            -d @- <<'JSON'
          {
            "fields": {
              "project": { "key": "'${JIRA_PROJECT_KEY}'" },
              "issuetype": { "name": "Bug" },
              "summary": "'${TITLE}'",
              "labels": ["ci","kintsugi"],
              "description": { "type": "doc", "version": 1,
                "content":[{"type":"paragraph","content":[{"text":"'${BODY}'","type":"text"}]}]
              }
            }
          }
JSON
```

## PR/Branch Naming
- Use the Jira key in branch/PR titles: `MQS-123: ...` for auto-linking.

## Backlog Seeding
- MQS-1 Hotfix: Fix YAML parse at line 166 & artifact naming
- MQS-2 Bug: VS Code “too many active changes” — add .gitignore, snapshot branch, chunked commits
- MQS-3 Task: CloneForClientReady baseline plan (Accenture)
- MQS-4 Task: UI “Run All” stabilization
- MQS-5 Task: Docs parity & 4444-summary inclusion
- MQS-6 Spike: InnerCouncil → decision engine (design doc)

## Decision Log
- Log the “Jira online” gate in `docs/decision_log.md`.
