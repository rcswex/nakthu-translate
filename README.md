# nakthu-translate

**A Claude skill that translates text into Nakthu (梦天语), a constructed language — faithfully, fluently, elegantly.**
**把原文（主要是中文）按「信、达、雅」译进梦天语的 Claude skill。**

[English](#english) · [中文](#中文)

> Nakthu · 梦天语 — project site / 项目主页: <https://rcswex.github.io/nakthu/>

---

## English

### What is this?

[Nakthu](https://rcswex.github.io/nakthu/) (`Nāk-θụʔ`, "human language") is an experimental constructed language built with a *sandbox method*: instead of coining words one by one, a fifty-person lakeside settlement is simulated for a hundred years, and every grammatical feature is added only when that society *has to* say something it could not say before. Its signatures:

- **A syllable is a grid point with four slots** — onset, nucleus, coda, tone. Words are read, not memorised: the slots encode texture, reachability, duration and operation.
- **Vowels run on two axes** (reachable / not, specified / not); length adds only "non-termination".
- **Evidentiality is obligatory.** An assertion must say how you know it (`-i:` seen, `-e:` heard, `-u:` felt, `-ei` hearsay …).
- **Words never translate word-for-word, but always translate.** Paths differ; landing points are shared.

This skill is a translator's workbench for that language. It makes Claude work the way the project's own translators do: read the archive, find the *landing point* of each word, choose a register, assemble short paths, check every form against the lexicon, and report honestly what was lost.

### Features

| Mode | Command | Output |
|---|---|---|
| default | `/nakthu-translate <text>` | per stanza: **Nakthu · word-by-word gloss · landing reading** |
| `-only` | `/nakthu-translate -only <text>` | **Nakthu text only** |
| `-doc` | `/nakthu-translate -doc <text>` | a **Markdown document**: original, translation, interlinear gloss, landing reading, commentary, additions & omissions, ✧ provisional-word table, proofreading notes — in the layout of the project's *遇到* and *至圣先师歌* translations |

Other options: `-style=<register>` (one of 22 registers), `-out=<path>` (for `-doc`), `-root=<path>` (archive root).

Also included:

- **Translation craft** distilled from the project's *Literature & Translation Compendium*: two laws of translation, the four-step method, the five prohibitions, "keep the image", reduplication rules, the "never say *unsayable*" discipline, a loss ledger.
- **`scripts/nakthu_lex.py`** (stdlib-only Python):
  - `lookup` — find a form or a Chinese gloss in the lexicons;
  - `check` — verify that every form is attested, one syllable per hyphen-unit, and that provisional words stay under 5 %;
  - `coin` — register newly coined **✧ words** into `_temp/新铸词列表.md` (rejects collisions and same-form/different-sense clashes).

### Requirements

1. **[Claude Code](https://docs.claude.com/en/docs/claude-code)** (CLI, desktop app or IDE extension).
2. **Python 3.8+** on `PATH` (as `python`).
3. **The Nakthu archive** — *not* bundled here. The skill reads, at run time, from a directory that contains a `language/` folder with at least:
   - `梦天语分级词典.md`, `梦天语词典.md`, `临时词账.md` (lexicons),
   - `_grammar_book/梦天语词法手册.md` (grammar handbook),
   - ideally also the main book and the *Compendium* (see the [project site](https://rcswex.github.io/nakthu/)).

   Point the skill at it with the `NAKTHU_ROOT` environment variable (or `-root=`). Default: `F:\金盘\Nakthu`.

Without the archive the skill can still explain its method, but it will refuse to invent forms — it cannot verify them.

### Installation

**Option A — as a Claude Code plugin (recommended for sharing)**

```text
/plugin marketplace add rcswex/nakthu-translate-skill
/plugin install nakthu-translate@nakthu-translate
```

**Option B — as a personal skill (local, no marketplace)**

```powershell
git clone https://github.com/rcswex/nakthu-translate-skill.git
cd nakthu-translate-skill
powershell -ExecutionPolicy Bypass -File .\install.ps1      # Windows
# sh install.sh                                             # macOS / Linux
```

This copies `skills/nakthu-translate/` to `~/.claude/skills/nakthu-translate/`. Or copy that folder by hand.

**Option C — project-level**

Copy `skills/nakthu-translate/` into `<your-project>/.claude/skills/`.

Then set the archive location (once):

```powershell
setx NAKTHU_ROOT "D:\path\to\Nakthu"      # Windows (new shells)
# export NAKTHU_ROOT=/path/to/Nakthu       # macOS / Linux
```

Verify:

```powershell
python "$HOME\.claude\skills\nakthu-translate\scripts\nakthu_lex.py" where
```

### Usage

```text
/nakthu-translate 你身上专属的陌生味道，是我确认你存在的目标。
/nakthu-translate -only 山不走，人走。
/nakthu-translate -doc -style=风雅体 枯藤老树昏鸦，小桥流水人家。
/nakthu-translate -doc F:\poems\遇到.txt -out=F:\out\遇到_梦天语译.md
```

Or just ask in natural language: "translate this into Nakthu", "译成梦天语".

New coinages are logged to `<archive root>/_temp/新铸词列表.md`.

### Repository layout

```text
.claude-plugin/
  plugin.json                  plugin manifest
  marketplace.json             single-plugin marketplace
skills/nakthu-translate/
  SKILL.md                     the skill (arguments, workflow, hard rules)
  references/
    translation-craft.md       laws, 4-step method, prohibitions, register chooser
    grammar-card.md            quick grammar card (the handbook is authoritative)
    output-formats.md          templates for the three modes + coinage list
  scripts/nakthu_lex.py        lookup / check / coin
install.ps1 · install.sh       local installers
```

### Honest limits

- `check` verifies **forms and syllable structure only**. It cannot prove a sentence grammatical; Claude is instructed to check syntax against the handbook, and to list every "extrapolated" construction in the proofreading notes.
- The skill treats the lexicon and handbook as authoritative; the example translations are *layout* models, not lexical authorities (e.g. the old 2nd person `tə́k` is superseded by `nī`).
- Quality tracks the archive: if the archive is out of date, so is the output.

### License

No licence has been chosen yet; until the repository owner adds a `LICENSE` file, all rights are reserved. The Nakthu language and its archive belong to their creator and are **not** included.

---

## 中文

### 这是什么

[梦天语](https://rcswex.github.io/nakthu/)（Nakthu，本语自名 `Nāk-θụʔ`，「人语」）是一门基于语言决定论与**沙盒法**设计的造语：不为概念配词，而是设一个约五十人的湖畔聚落，让它走一百年，看这个社会什么时候**非说不可**，语法才长出一项。它的几个签名：

- **一格一音节，四个槽**：起首、韵核、韵尾、声调。词是读出来的，不是背出来的；
- **元音走两根轴**（够得着／够不着，指定／不指定），长音只加「不终止」；
- **断言必须作证**：说一句话，要说出你怎么知道的（`-i:` 亲眼、`-e:` 亲耳、`-u:` 亲身、`-ei` 传闻……）；
- **词永远不能逐词对译，永远可以被译出**：路径无一相同，落点是共享的。

本 skill 是这门语言的**译者工作台**：让 Claude 像项目自己的译者那样工作——先读档案，认每个词的**落点**，定文体，配短弯，逐词查词典，最后诚实交代丢了什么。

### 功能

| 模式 | 调用 | 输出 |
|---|---|---|
| 默认 | `/nakthu-translate <原文>` | 每节：**梦天语 · 逐字译 · 落点读** |
| `-only` | `/nakthu-translate -only <原文>` | **仅梦天语** |
| `-doc` | `/nakthu-translate -doc <原文>` | **MD 文档**：原文、译文、逐词直译、落点读、译解、增减与补注、✧ 临时词表、校记，体例参照《遇到_梦天语译》《至圣先师歌_梦天语译》 |

另有 `-style=<文体>`（22 体之一）、`-out=<路径>`（配合 `-doc`）、`-root=<路径>`（档案根目录）。

附带：

- **翻译手艺**，提炼自《文学与翻译汇编》：两定律、四步法、五禁例、意象照翻、叠字二分、「不写说不出」的纪律、损失清单；
- **`scripts/nakthu_lex.py`**（纯标准库 Python）：
  - `lookup` 按词形或汉义查词；
  - `check` 校验词形是否在册、连字符单元是否一格一音节、临时词占比是否 ≤ 5%；
  - `coin` 把新铸的 **✧ 词**登记到 `_temp/新铸词列表.md`（自动拦截撞形与同形两义）。

### 前置条件

1. **[Claude Code](https://docs.claude.com/en/docs/claude-code)**（命令行、桌面应用或 IDE 扩展均可）。
2. **Python 3.8+**，命令名 `python` 在 `PATH` 中。
3. **梦天语档案**——**本仓库不含**。skill 在运行时读取一个含 `language/` 子目录的根目录，至少需要：
   - `梦天语分级词典.md`、`梦天语词典.md`、`临时词账.md`（词典）；
   - `_grammar_book/梦天语词法手册.md`（词法手册）；
   - 最好还有主书与《文学与翻译汇编》（见[项目主页](https://rcswex.github.io/nakthu/)）。

   用环境变量 `NAKTHU_ROOT`（或 `-root=`）指向它；默认 `F:\金盘\Nakthu`。

没有档案时，skill 仍能讲方法，但**会拒绝凭空造词形**——它无从核对。

### 安装

**方式 A：作为 Claude Code 插件（便于分享）**

```text
/plugin marketplace add rcswex/nakthu-translate-skill
/plugin install nakthu-translate@nakthu-translate
```

**方式 B：个人 skill（本地使用，无需 marketplace）**

```powershell
git clone https://github.com/rcswex/nakthu-translate-skill.git
cd nakthu-translate-skill
powershell -ExecutionPolicy Bypass -File .\install.ps1      # Windows
# sh install.sh                                             # macOS / Linux
```

它会把 `skills/nakthu-translate/` 复制到 `~/.claude/skills/nakthu-translate/`；手动复制该目录也一样。

**方式 C：项目级**

把 `skills/nakthu-translate/` 复制到 `<你的项目>/.claude/skills/`。

然后设置一次档案位置：

```powershell
setx NAKTHU_ROOT "D:\path\to\Nakthu"      # Windows（新开终端生效）
# export NAKTHU_ROOT=/path/to/Nakthu       # macOS / Linux
```

验证：

```powershell
python "$HOME\.claude\skills\nakthu-translate\scripts\nakthu_lex.py" where
```

### 使用

```text
/nakthu-translate 你身上专属的陌生味道，是我确认你存在的目标。
/nakthu-translate -only 山不走，人走。
/nakthu-translate -doc -style=风雅体 枯藤老树昏鸦，小桥流水人家。
/nakthu-translate -doc F:\poems\遇到.txt -out=F:\out\遇到_梦天语译.md
```

也可以直接说「把这段译成梦天语」。译写中新铸的词登记在 `<档案根>/_temp/新铸词列表.md`。

### 目录结构

```text
.claude-plugin/
  plugin.json                  插件清单
  marketplace.json             单插件 marketplace
skills/nakthu-translate/
  SKILL.md                     skill 本体（参数、工作流、硬规则）
  references/
    translation-craft.md       定律、四步法、禁例、文体选择表
    grammar-card.md            语法速查卡（以词法手册为准）
    output-formats.md          三种模式与新铸词列表的模板
  scripts/nakthu_lex.py        查词 / 校验 / 登记
install.ps1 · install.sh       本地安装脚本
```

### 诚实的边界

- `check` 只核**词形与一格一音节**，不能证明句子合乎语法。skill 要求 Claude 对照词法手册自查语法，并把「译者往前推」的句式逐条写进校记。
- 词典与词法手册是权威；范文只是**体例**范本，不是词形权威（例如旧第二人称 `tə́k` 已由 `nī` 取代）。
- 产出质量随档案：档案旧，译文就旧。

### 许可

尚未选定许可证；仓库所有者添加 `LICENSE` 之前，保留所有权利。梦天语及其档案归创制者所有，**不在本仓库内**。

### 链接

- 梦天语项目主页：<https://rcswex.github.io/nakthu/>
