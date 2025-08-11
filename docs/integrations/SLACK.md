# Slack Integration Guide

## Option A — GitHub App (fastest)
- Install the official GitHub app in Slack.
- Subscribe the channel to your repo’s events (PRs/commits).

## Option B — CI Failure Notification (recommended)
- In Slack: create an Incoming Webhook → copy URL.
- In GitHub repo → Settings → Secrets and variables → Actions → add:
  - SLACK_WEBHOOK_URL
- Append to `.github/workflows/tests.yml`:
```yaml
  slack:
    name: slack (on failure)
    needs: [tests]
    if: ${{ failure() && secrets.SLACK_WEBHOOK_URL != '' }}
    runs-on: ubuntu-latest
    steps:
      - name: Post failure to Slack
        env:
          WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          REF_NAME: ${{ github.ref_name }}
          WORKFLOW: ${{ github.workflow }}
          RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
        run: |
          printf '{"text":":x: *CI failed* on `%s` for *%s*.\nRun: %s\nArtifacts: reports/ & screenshots/"}' \
            "$REF_NAME" "$WORKFLOW" "$RUN_URL" > payload.json
          curl -s -X POST -H 'Content-type: application/json' --data @payload.json "$WEBHOOK_URL"
```

## Channels
- #ci-alerts — bot posts from Actions (fail or green)
- #qa-lab — human chatter, triage, links to artifacts
- #client-baselines — notes when you spin a client clone
