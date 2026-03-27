# AI Workflows for Argentum Online

Reusable GitHub Actions workflows for AI-powered issue fixing, using DeepSeek as the LLM provider.

## Setup

### 1. Add secrets to your repos

In each repo (client, server), add these secrets under Settings → Secrets → Actions:

| Secret | Required | Purpose |
|--------|----------|---------|
| `DEEPSEEK_API_KEY` | Yes | DeepSeek API key |
| `JENKINS_USER` | For retry | Jenkins API username |
| `JENKINS_TOKEN` | For retry | Jenkins API token |

### 2. Add workflow files to each repo

Create `.github/workflows/ai-fix.yml` in your client/server repos:

```yaml
name: AI Fix Issue

on:
  issues:
    types: [labeled]

jobs:
  ai-fix:
    if: >
      github.event.label.name == 'ai-fix' &&
      github.event.issue.author_association != 'NONE'
    uses: ao-org/argentum-online-assets/.github/workflows/ai-fix-reusable.yml@main
    secrets:
      DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
```

Create `.github/workflows/ai-fix-retry.yml` for Jenkins retry:

```yaml
name: AI Fix Build Errors

on:
  status:

jobs:
  ai-retry:
    uses: ao-org/argentum-online-assets/.github/workflows/ai-fix-retry-reusable.yml@main
    secrets:
      DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
      JENKINS_USER: ${{ secrets.JENKINS_USER }}
      JENKINS_TOKEN: ${{ secrets.JENKINS_TOKEN }}
```

## Usage

1. Create an issue describing the bug or feature
2. Add the `ai-fix` label to the issue
3. The workflow will:
   - Read all VB6 files from the repo
   - Fetch coding standards from the Recursos repo
   - Send everything to DeepSeek
   - Create a PR with the fix
4. If Jenkins build fails, the retry workflow will:
   - Fetch the build error log
   - Send errors to DeepSeek for fixing
   - Push the fix to the same branch
   - Retry up to 3 times

## Files

```
tools/ai_auto_pr_fix/
├── scripts/
│   ├── ai-fix.mjs                 # Main AI fix script
│   └── ai-fix-retry.mjs           # Retry script for build errors
└── README.md

.github/workflows/
├── ai-fix-reusable.yml            # Main reusable workflow (issue → PR)
└── ai-fix-retry-reusable.yml      # Retry reusable workflow (build fail → fix)
```
