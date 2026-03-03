param(
  [string]$BaseBranch = "main",
  [string]$LocalizationBranch = "localization-zh-cn"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "[1/4] 获取最新代码..."
git fetch --all --prune | Out-Null

Write-Host "[2/4] 切换到 $BaseBranch 并更新..."
git checkout $BaseBranch | Out-Null
git pull --ff-only | Out-Null

Write-Host "[3/4] 应用汉化提交..."
$commit = "c977b91"

git merge-base --is-ancestor $commit HEAD
if ($LASTEXITCODE -eq 0) {
  Write-Host "ℹ️ 当前分支已包含汉化提交: $commit，跳过回放。"
}
else {
  try {
    git cherry-pick $commit | Out-Null
    Write-Host "✅ 已应用汉化提交: $commit"
  }
  catch {
    Write-Warning "⚠️ cherry-pick 冲突，请手动解决后执行: git cherry-pick --continue"
    exit 1
  }
}

Write-Host "[4/4] 同步汉化分支快照..."
git branch -f $LocalizationBranch HEAD

Write-Host "\n完成：升级后已自动回放汉化。" -ForegroundColor Green
