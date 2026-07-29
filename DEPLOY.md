# Deploying

## Verify what you have

In the extracted folder:

```bash
python3 scripts/check-deployment.py
```

Expect `version 3.2.0`, `layout self-contained plugin dirs`, `15 plugins`, `67 skills`, `OK`.

If it reports `layout shared root (old)`, you are on a pre-3.0.0 build.

## Copy into your repo

The one thing that goes wrong: `.claude-plugin/` is a hidden dot-directory and Explorer drag-and-drop skips it. Use `robocopy /E`, or the scripts below, which verify afterwards and fail loudly.

**PowerShell**
```powershell
.\deploy.ps1 -Repo D:\AIAutomation\your-repo -Push
```

**Python (no execution policy involved)**
```powershell
python deploy.py D:\AIAutomation\your-repo --push
```

**By hand**
```powershell
cd D:\AIAutomation\your-repo
Get-ChildItem -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force
robocopy D:\Downloads\qz-agent-clusters . /E /XD .git
python scripts\check-deployment.py
git add -A; git commit -m "Deploy 3.0.0"; git push
```

If the build is already sitting inside the repo, skip the copy entirely — just verify and push. Both scripts refuse to run when source and target are the same folder.

## Refresh the client

Pushing is not enough; the marketplace is cached locally.

```
/plugin marketplace update qz-agent-clusters
/reload-plugins
```

If it still shows the old catalog:

```
/plugin marketplace remove qz-agent-clusters
/plugin marketplace add Qualizeal/skills
```

## Confirm

`qa-knowledge-fabric` should show **5 skills**: `artefact-ingestion`, `tagging-vocabulary`, `retrieval-chunking`, `redaction-policy`, `retrieval-quality-audit`.

`qa-playwright-automation` should show **5**: `playwright-operating-rules`, `playwright-framework`, `playwright-locator-strategy`, `playwright-script-generation`, `playwright-mcp`.

A single skill named after the plugin means an older build is still live.
