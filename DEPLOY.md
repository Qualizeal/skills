# Deploying an update

The panel shows whatever the **deployed** `marketplace.json` says. The version badge tells you which build is live:

| Badge | Build | Skills per plugin |
|---|---|---|
| `0.1.0` | 4 cluster plugins | 1 (broken — pointed at a parent folder) |
| `1.0.0` | 15 plugins | 1 each |
| `2.0.0` | 15 plugins | 3-7 each, 67 total |

If it does not say `2.0.0`, the repository has not been updated — no client-side action will change that.

## The step that is usually missed

`.claude-plugin/` is a hidden dot-directory. Copying the folder in Windows Explorer with "Hidden items" unticked silently leaves the old `marketplace.json` in place. You then get the new skill tree with the old catalog describing it — every plugin shows one skill, pointing at a directory that no longer contains a `SKILL.md`.

`scripts/check-deployment.py` detects exactly this and names it a MIXED STATE.

## Replace the repository contents

Delete everything except `.git`, then copy this build in whole.

**PowerShell**

```powershell
cd D:\AIAutomation\your-marketplace-repo

# remove everything except .git
Get-ChildItem -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force

# copy the extracted build in, including hidden directories
robocopy D:\path\to\qz-agent-clusters . /E /XD .git

git add -A
git commit -m "Restructure: task-level skills, 67 across 15 plugins"
git push
```

`robocopy /E` copies hidden directories. `xcopy` and drag-and-drop may not.

**Verify before pushing**

```powershell
python scripts\check-deployment.py
```

Expect: `version 2.0.0`, `plugins 15`, `skills 67 claimed / 67 on disk`, verdict `Current.`

If it reports a MIXED STATE or a count other than 67, `.claude-plugin/marketplace.json` did not get replaced.

## Refresh the client

Pushing is not enough — the marketplace is cached locally.

```
/plugin marketplace update qz-agent-clusters
/reload-plugins
```

If the panel still shows the old version, force a clean clone:

```
/plugin marketplace remove qz-agent-clusters
/plugin marketplace add Qualizeal/skills
```

Removing a marketplace uninstalls plugins that came from it; reinstall the ones you want afterwards.

## Confirm it worked

`qa-knowledge-fabric` should expand to five skills:

```
artefact-ingestion
tagging-vocabulary
retrieval-chunking
redaction-policy
retrieval-quality-audit
```

If it shows one skill called `knowledge-fabric`, you are still on 1.0.0.
