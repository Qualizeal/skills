# Running the deploy script on Windows

## 1. Extract the zip properly

Right-click the zip → **Extract All**. Do not work inside the zip preview window — scripts run from there fail in confusing ways.

## 2. Open PowerShell in the extracted folder

In File Explorer, navigate into the folder that contains `deploy.ps1`, then either:

- Type `powershell` in the address bar and press Enter, or
- Shift + right-click in empty space → **Open PowerShell window here**

Confirm you are in the right place:

```powershell
dir deploy.ps1
```

## 3. Unblock the files

**This is the fix for "is not digitally signed".** That error means Windows still has the file marked as downloaded from the internet, so `RemoteSigned` refuses to run it. Unblock it in the folder the script actually lives in:

```powershell
Get-ChildItem -Recurse | Unblock-File
```

If the error persists, check which policy is in force:

```powershell
Get-ExecutionPolicy -List
```

- `RemoteSigned` at `CurrentUser` or `LocalMachine` → `Unblock-File` above resolves it.
- `AllSigned` → even local unsigned scripts are blocked. Try `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- A value under `MachinePolicy` or `UserPolicy` → set by your IT group policy and **cannot** be overridden by any scope. Use the Python version instead; execution policy does not apply to it:

```powershell
python deploy.py D:\AIAutomation\your-repo --push
```

### Original step 3

Anything extracted from a downloaded zip is marked as internet-sourced, and PowerShell refuses to run it:

```powershell
Get-ChildItem -Recurse | Unblock-File
```

## 4. Run it

The `.\` prefix is required — PowerShell will not run a script from the current directory without it.

```powershell
.\deploy.ps1 -Repo D:\AIAutomation\my-agent-marketplace
```

If you get **"running scripts is disabled on this system"**, allow it for this window only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\deploy.ps1 -Repo D:\AIAutomation\my-agent-marketplace
```

`-Scope Process` lasts until you close the window and changes nothing permanently.

Or in a single command without changing any policy:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy.ps1 -Repo D:\AIAutomation\my-agent-marketplace
```

## 5. Commit and push

Add `-Push` once the dry run looks right:

```powershell
.\deploy.ps1 -Repo D:\AIAutomation\my-agent-marketplace -Push
```

## What success looks like

```
Source : D:\Downloads\qz-agent-clusters
Target : D:\AIAutomation\my-agent-marketplace
Build  : 2.0.0

Clearing target (keeping .git)...
Copying build (hidden directories included)...

Deployed:
  version : 2.0.0
  plugins : 15
  skills  : 67 claimed / 67 on disk
  status  : OK
```

Anything other than `67 claimed / 67 on disk` and `status OK` means it did not deploy cleanly, and the script stops rather than leaving you with a half-updated repo.

Then, in Claude Code:

```
/plugin marketplace update qz-agent-clusters
/reload-plugins
```

## If PowerShell is locked down

Corporate policy can block scripts in a way `-Scope Process` cannot override. Use the Python version instead — same checks, no execution policy involved:

```powershell
python deploy.py D:\AIAutomation\my-agent-marketplace --push
```

## If you would rather do it by hand

Three commands. The `/E` flag is the important one: it copies hidden directories such as `.claude-plugin`, which is what Explorer drag-and-drop misses.

```powershell
cd D:\AIAutomation\my-agent-marketplace
Get-ChildItem -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force
robocopy D:\Downloads\qz-agent-clusters . /E /XD .git
```

Then verify before pushing:

```powershell
python scripts\check-deployment.py
```
