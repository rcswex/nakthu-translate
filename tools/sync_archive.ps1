# 维护者用：把梦天语活档案同步进 skills/nakthu-translate/archive/ 快照。
# 用法：powershell -ExecutionPolicy Bypass -File .\tools\sync_archive.ps1 -Source "F:\金盘\Nakthu"
param(
  [Parameter(Mandatory = $true)][string]$Source
)
$ErrorActionPreference = "Stop"
$lang = Join-Path $Source "language"
if (-not (Test-Path (Join-Path $lang "梦天语词典.md"))) { throw "$Source 下没有 language\梦天语词典.md" }
$dst = Join-Path $PSScriptRoot "..\skills\nakthu-translate\archive\language"
$dst = [System.IO.Path]::GetFullPath($dst)

$top = @(
  "梦天语分级词典.md", "梦天语词典.md", "临时词账.md", "梦天语语言概况.md",
  "梦天语文体示例集.md", "梦天语寒暄与应对语定稿.md", "梦天语十课通稿.md", "梦天语绪论课.md",
  "梦天语（Nakthu）：一门旨在加速人类进步的造语.md",
  "梦天语（Nakthu）文学与翻译汇编【上册】.md"
)
$zhihu = @(
  "遇到_梦天语译.md", "至圣先师歌_梦天语译.md", "梦天语哲理句辑.md",
  "梦天语（Nakthu）文体介绍之“浮艳风”.md"
)
New-Item -ItemType Directory -Force -Path "$dst\_grammar_book", "$dst\_zhihu" | Out-Null
foreach ($f in $top)   { Copy-Item -Force (Join-Path $lang $f) $dst }
foreach ($f in $zhihu) { Copy-Item -Force (Join-Path $lang "_zhihu\$f") "$dst\_zhihu" }
Copy-Item -Force (Join-Path $lang "_grammar_book\梦天语词法手册.md") "$dst\_grammar_book"
Write-Host "已同步到 $dst"
Write-Host "记得更新 archive\README.md 的快照日期，再 git commit。"
