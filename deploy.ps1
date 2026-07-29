<#
.SYNOPSIS
  Deploy this build into a marketplace repo, correctly, including hidden directories.

.EXAMPLE
  .\deploy.ps1 -Repo D:\AIAutomation\my-agent-marketplace
  .\deploy.ps1 -Repo D:\AIAutomation\my-agent-marketplace -Push
#>
param(
  [Parameter(Mandatory=$true)][string]$Repo,
  [switch]$Push
)

$ErrorActionPreference = 'Stop'
$Source = $PSScriptRoot

Write-Host "Source : $Source"
Write-Host "Target : $Repo`n"

if (-not (Test-Path (Join-Path $Source '.claude-plugin\marketplace.json'))) {
  throw "No .claude-plugin\marketplace.json in $Source. Extract the zip fully and run this from inside the extracted folder."
}
if (-not (Test-Path $Repo)) { throw "Target repo not found: $Repo" }

# Refuse to run if source and target overlap. Clearing the target would delete
# the source, leaving nothing to copy from.
$srcFull  = (Resolve-Path $Source).Path.TrimEnd('\\')
$repoFull = (Resolve-Path $Repo).Path.TrimEnd('\\')
if ($srcFull -eq $repoFull) {
  throw @"
Source and target are the same folder:
  $srcFull

The build is already sitting in the repo, so there is nothing to deploy.
Verify and push instead:

  python scripts\check-deployment.py
  git add -A; git commit -m "Update marketplace"; git push
"@
}
if ($repoFull.StartsWith($srcFull + [IO.Path]::DirectorySeparatorChar) -or
    $srcFull.StartsWith($repoFull + [IO.Path]::DirectorySeparatorChar)) {
  throw "Source and target are nested ($srcFull / $repoFull). Extract the build somewhere separate, such as your Downloads folder, and run it from there."
}

$srcVersion = (Get-Content (Join-Path $Source '.claude-plugin\marketplace.json') -Raw | ConvertFrom-Json).version
Write-Host "Deploying build $srcVersion" -ForegroundColor Cyan

# 1. Clear the repo except .git
Write-Host "Clearing target (keeping .git)..."
Get-ChildItem -Path $Repo -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force

# 2. Copy everything INCLUDING hidden dot-directories. /E does subdirs, empty ones too.
Write-Host "Copying build (hidden directories included)..."
$null = robocopy $Source $Repo /E /XD .git /NFL /NDL /NJH /NJS /NP
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }

# 3. Verify the thing that actually matters
$manifest = Join-Path $Repo '.claude-plugin\marketplace.json'
if (-not (Test-Path $manifest)) {
  throw "FAILED: .claude-plugin\marketplace.json is missing from the target. The catalog was not deployed."
}
$mk = Get-Content $manifest -Raw | ConvertFrom-Json
$onDisk = (Get-ChildItem -Path (Join-Path $Repo 'plugins') -Recurse -Filter SKILL.md).Count

Write-Host "`nDeployed:"
Write-Host "  version : $($mk.version)"
Write-Host "  plugins : $($mk.plugins.Count)"
Write-Host "  skills  : $onDisk discovered"

foreach ($p in $mk.plugins) {
  $pj = Join-Path $Repo (Join-Path $p.source '.claude-plugin\plugin.json')
  if (-not (Test-Path $pj)) { throw "Missing plugin.json for $($p.name)" }
}
if ($onDisk -ne 67) { throw "Expected 67 skills, found $onDisk." }
if ($mk.version -ne $srcVersion) { throw "Version mismatch after copy - the manifest was not replaced." }
Write-Host "  status  : OK" -ForegroundColor Green

# 4. Optionally commit and push
if ($Push) {
  Push-Location $Repo
  git add -A
  git commit -m "Deploy qz-agent-clusters $($mk.version)"
  git push
  Pop-Location
  Write-Host "`nPushed. Now run in Claude Code:" -ForegroundColor Yellow
} else {
  Write-Host "`nNot pushed (pass -Push to commit and push). Then run in Claude Code:" -ForegroundColor Yellow
}
Write-Host "  /plugin marketplace update $($mk.name)"
Write-Host "  /reload-plugins"
