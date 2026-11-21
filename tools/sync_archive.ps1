# 维护者用：把梦天语活档案（中文文件名）同步进 skills/nakthu-translate/archive/ 快照（ASCII 文件名）。
# 快照用 ASCII 名，是因为 Claude Chat 的 skill 上传不接受含中文的 zip 路径。
# 用法：powershell -ExecutionPolicy Bypass -File .\tools\sync_archive.ps1 -Source "F:\金盘\Nakthu"
param(
  [Parameter(Mandatory = $true)][string]$Source
)
$ErrorActionPreference = "Stop"
$lang = Join-Path $Source "language"
if (-not (Test-Path (Join-Path $lang "梦天语词典.md"))) { throw "$Source 下没有 language\梦天语词典.md" }
$dst = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\skills\nakthu-translate\archive\language"))
New-Item -ItemType Directory -Force -Path "$dst\_grammar_book", "$dst\_zhihu" | Out-Null

# 活档案中文名 -> 快照 ASCII 名（相对 language\）
$map = [ordered]@{
  "梦天语分级词典.md"                                   = "graded-dictionary.md"
  "梦天语词典.md"                                       = "dictionary.md"
  "临时词账.md"                                         = "provisional-ledger.md"
  "梦天语语言概况.md"                                   = "overview.md"
  "梦天语文体示例集.md"                                 = "register-samples.md"
  "梦天语寒暄与应对语定稿.md"                           = "greetings.md"
  "梦天语十课通稿.md"                                   = "ten-lessons.md"
  "梦天语绪论课.md"                                     = "intro-lesson.md"
  "梦天语（Nakthu）：一门旨在加速人类进步的造语.md"     = "main-book.md"
  "梦天语（Nakthu）文学与翻译汇编【上册】.md"           = "compendium.md"
  "_grammar_book\梦天语词法手册.md"                     = "_grammar_book\grammar-handbook.md"
  "_zhihu\遇到_梦天语译.md"                             = "_zhihu\yudao_nakthu.md"
  "_zhihu\至圣先师歌_梦天语译.md"                       = "_zhihu\zhishengxianshi-ge_nakthu.md"
  "_zhihu\梦天语哲理句辑.md"                            = "_zhihu\aphorisms.md"
  "_zhihu\梦天语（Nakthu）文体介绍之“浮艳风”.md"       = "_zhihu\fuyan-style.md"
}
foreach ($k in $map.Keys) {
  $from = Join-Path $lang $k
  if (-not (Test-Path $from)) { Write-Warning "缺少 $from，跳过"; continue }
  Copy-Item -Force $from (Join-Path $dst $map[$k])
}
Write-Host "已同步到 $dst"
Write-Host "记得更新 archive\README.md 的快照日期，再 git commit。"
