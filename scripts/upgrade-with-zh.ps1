param(
  [string]$BaseBranch = "main"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "开始升级并保留汉化..." -ForegroundColor Cyan
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "reapply-zh.ps1") -BaseBranch $BaseBranch -LocalizationBranch "localization-zh-cn"

Write-Host "\n当前状态：" -ForegroundColor Cyan
git --no-pager log --oneline -n 3
