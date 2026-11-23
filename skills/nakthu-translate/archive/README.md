# archive · 梦天语档案快照 / Nakthu archive snapshot

本目录是 `nakthu-translate` 自带的**梦天语档案快照**，让 skill 自足，不依赖外部文件。
This directory is the **self-contained snapshot of the Nakthu archive** bundled with the skill.

- 快照日期 / Snapshot: 2026-11-22
- 来源 / Source: 创制者的活档案 `language/`（词典 937 条口径：分级词典正文 900 条 ＋ 词账 37 枚回补）
- 项目主页 / Project site: <https://rcswex.github.io/nakthu/>

| 文件 | 内容 |
|---|---|
| `language/_grammar_book/grammar-handbook.md`（梦天语词法手册） | 词法手册：成熟梦天语的最新语法（权威） |
| `language/graded-dictionary.md`（梦天语分级词典） | 分级词典（十级） |
| `language/dictionary.md`（梦天语词典） | 词典 |
| `language/provisional-ledger.md`（临时词账） | ✧ 临时词账与 37 枚回补名单 |
| `language/main-book.md`（梦天语（Nakthu）：一门旨在加速人类进步的造语） | 主书 v1.5 |
| `language/compendium.md`（梦天语（Nakthu）文学与翻译汇编【上册】） | 文学与翻译汇编 |
| `language/overview.md`（语言概况）· `register-samples.md`（文体示例集）· `greetings.md`（寒暄与应对语定稿） | 概况、文体样例、寒暄 |
| `language/ten-lessons.md`（十课通稿）· `intro-lesson.md`（绪论课） | 教材 |
| `language/_zhihu/`：`yudao_nakthu.md`（遇到_梦天语译）· `zhishengxianshi-ge_nakthu.md`（至圣先师歌_梦天语译）· `aphorisms.md`（哲理句辑）· `fuyan-style.md`（文体介绍之浮艳风） | 范文：《遇到》《至圣先师歌》，及哲理句辑、浮艳风文体介绍 |

## 说明 / Notes

- 文件名用 ASCII：Claude Chat 上传 zip 时会拒绝含中文的路径。作者的活档案用中文文件名，`nakthu_lex.py` 两种都认；`tools/sync_archive.ps1` 负责改名同步。
  File names are ASCII because Claude Chat rejects zip paths with non-ASCII characters. The author's live archive uses Chinese names; `nakthu_lex.py` accepts both.

- 这是**快照**。活档案若更新，用仓库根目录的 `tools/sync_archive.ps1` 重新同步；或设环境变量 `NAKTHU_ROOT` 指向活档案，skill 会优先用它。
  This is a snapshot. To refresh it use `tools/sync_archive.ps1`, or point `NAKTHU_ROOT` at the live archive (it takes precedence).
- 档案内部偶有指向其他工作稿的引用（如“见某某定稿”），快照里可能没有那份文件；以本目录内的词法手册、词典为准。
- 不要手改本目录里的文件；改动应回到活档案，再同步。
- 许可 / License：本仓库整体采用 MIT 许可证，见根目录 `LICENSE`，档案快照在内。 The whole repository, this snapshot included, is under the MIT licence (see `LICENSE` at the repo root).
