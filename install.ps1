# 安装 nakthu-translate skill 到 Claude 本地（用户级）。
# 用法：powershell -ExecutionPolicy Bypass -File .\install.ps1 [-Target <skills 目录>]
param(
  [string]$Target = (Join-Path $env:USERPROFILE ".claude\skills")
)
$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "skills\nakthu-translate"
$dst = Join-Path $Target "nakthu-translate"
if (-not (Test-Path $src)) { throw "找不到 $src" }
New-Item -ItemType Directory -Force -Path $Target | Out-Null
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
Copy-Item -Recurse -Force $src $dst
Get-ChildItem -Recurse -Directory -Filter "__pycache__" $dst | Remove-Item -Recurse -Force
Write-Host "已安装到 $dst"
Write-Host "提示：设置环境变量 NAKTHU_ROOT 指向含 language\ 的梦天语档案根目录（默认 F:\金盘\Nakthu）。"
