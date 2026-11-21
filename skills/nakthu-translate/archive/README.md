# archive · 梦天语档案快照 / Nakthu archive snapshot

本目录是 `nakthu-translate` 自带的**梦天语档案快照**，让 skill 自足，不依赖外部文件。
This directory is the **self-contained snapshot of the Nakthu archive** bundled with the skill.

- 快照日期 / Snapshot: 2026-11-21
- 来源 / Source: 创制者的活档案 `language/`（词典 932 条口径：分级词典正文 895 条 ＋ 词账 37 枚回补）
- 项目主页 / Project site: <https://rcswex.github.io/nakthu/>

| 文件 | 内容 |
|---|---|
| `language/_grammar_book/梦天语词法手册.md` | 词法手册：成熟梦天语的最新语法（权威） |
| `language/梦天语分级词典.md` | 分级词典（十级） |
| `language/梦天语词典.md` | 词典 |
| `language/临时词账.md` | ✧ 临时词账与 37 枚回补名单 |
| `language/梦天语（Nakthu）：一门旨在加速人类进步的造语.md` | 主书 v1.5 |
| `language/梦天语（Nakthu）文学与翻译汇编【上册】.md` | 文学与翻译汇编 |
| `language/梦天语语言概况.md` · `梦天语文体示例集.md` · `梦天语寒暄与应对语定稿.md` | 概况、文体样例、寒暄 |
| `language/梦天语十课通稿.md` · `梦天语绪论课.md` | 教材 |
| `language/_zhihu/` | 范文：《遇到》《至圣先师歌》，及哲理句辑、浮艳风文体介绍 |

## 说明 / Notes

- 这是**快照**。活档案若更新，用仓库根目录的 `tools/sync_archive.ps1` 重新同步；或设环境变量 `NAKTHU_ROOT` 指向活档案，skill 会优先用它。
  This is a snapshot. To refresh it use `tools/sync_archive.ps1`, or point `NAKTHU_ROOT` at the live archive (it takes precedence).
- 档案内部偶有指向其他工作稿的引用（如“见某某定稿”），快照里可能没有那份文件；以本目录内的词法手册、词典为准。
- 不要手改本目录里的文件；改动应回到活档案，再同步。
- 版权与许可：档案的著作权归梦天语创制者所有；本仓库的许可见根目录说明。
