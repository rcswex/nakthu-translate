#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nakthu_lex.py - 梦天语译写辅助（仅标准库）

子命令
  where                         显示解析到的档案路径
  lookup <词形或汉字> [...]      查词：按转写词形（忽略调符也行）或按汉义
  check  <文件|->               校验一段梦天语转写：词形是否在册、一格一音节、占比
  coin   --form ... --gloss ... 把新铸 ✧ 词登记到 <根>/_temp/新铸词列表.md（先查撞形）

档案根目录解析顺序：--root > 环境变量 NAKTHU_ROOT > F:\\金盘\\Nakthu
（根目录下应有 language\\ 子目录；传入 language 目录本身也行）
"""
import argparse
import datetime as _dt
import os
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

DEFAULT_ROOT = r"F:\金盘\Nakthu"
GRADED = "梦天语分级词典.md"
DICT = "梦天语词典.md"
LEDGER = "临时词账.md"
COIN_REL = Path("_temp") / "新铸词列表.md"

TONE_MARKS = {"\u0304", "\u0300", "\u0301", "\u0309", "\u0303", "\u0323", "\u0302"}
CJK = re.compile(r"[\u4e00-\u9fff]")
HEAD_OK = re.compile(r"^[A-Za-zəɣʃθʔŋ\u0300-\u036f'ʼ:\-… !?]+$")
# 转写里的词素字符（含连字符与长音符）
TOKEN = re.compile(r"[A-Za-zəɣʃθʔŋ\u0300-\u036f'ʼ:\-]+")
VOWELS = set("aeiouəAEIOU")

# 词典未必逐条收、但正字法规定存在的封闭成分（零调，分写或连写）
FREE_ZERO = {
    # 座架 15
    "iu", "əu", "iə", "əi", "ei", "ui", "uə", "io", "uo", "eo", "əo", "oi", "ou", "oe", "oə",
    # 模态（座架长音形）
    "iu:", "əu:", "iə:", "əi:", "ei:", "ui:", "uə:", "io:", "uo:", "eo:", "əo:", "oi:", "ou:", "oe:", "oə:",
    # 量词
    "i:", "u:", "e:", "o:",
    # 真值算子
    "ʔaʔ", "ʔiʔ", "ʔuʔ", "ʔeʔ", "ʔoʔ", "ʔəʔ", "ʔa:ʔ", "ʔi:ʔ", "ʔu:ʔ", "ʔe:ʔ", "ʔo:ʔ", "ʔə:ʔ",
}
CLITIC_ZERO = {
    # 判据
    "i:", "u:", "e:", "mu:", "ui", "ei", "əu", "əi", "iu", "iə", "o:",
    # 信息结构 五短五长
    "əe", "ie", "ue", "eə", "eu", "əe:", "ie:", "ue:", "eə:", "eu:",
    # 其他附着
    "və", "ʃroθ", "nəm", "v", "w",
}
CLITIC_BASES = {"nəm", "lə"}  # 循格、过程小词：载调形都算


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def key(s: str) -> str:
    s = nfd(s.strip())
    return s.rstrip("…!?").strip()


def base(s: str) -> str:
    return "".join(ch for ch in nfd(s) if ch not in TONE_MARKS)


def vowel_groups(s: str) -> int:
    n, prev = 0, False
    for ch in base(s):
        v = ch in VOWELS
        if v and not prev:
            n += 1
        prev = v
    return n


def resolve_root(arg):
    for c in (arg, os.environ.get("NAKTHU_ROOT"), DEFAULT_ROOT):
        if not c:
            continue
        p = Path(c)
        if p.name == "language" and p.is_dir():
            p = p.parent
        if (p / "language").is_dir():
            return p
    sys.exit("找不到梦天语档案根目录（应含 language\\ 子目录）。请用 --root 或设置环境变量 NAKTHU_ROOT。")


class Lex:
    def __init__(self, root: Path):
        self.root = root
        self.lang = root / "language"
        self.entries = {}   # key -> [entry]
        self.by_base = {}   # base -> set(form)
        self.coined = {}    # key -> row dict  (新铸词列表 + 词账 ✧)
        self.loaded = []
        self._load_dict(self.lang / GRADED, "分级", graded=True)
        self._load_dict(self.lang / DICT, "词典", graded=False)
        self._load_ledger(self.lang / LEDGER)
        self._load_coin_list(root / COIN_REL)

    # -- 加载 -------------------------------------------------------
    def _add(self, form, level, src, text, gloss=""):
        k = key(form)
        e = {"form": form, "level": level, "src": src, "text": text, "gloss": gloss}
        self.entries.setdefault(k, []).append(e)
        self.by_base.setdefault(base(k), set()).add(form)

    def _load_dict(self, path: Path, src: str, graded: bool):
        if not path.exists():
            print(f"[警告] 缺少 {path}", file=sys.stderr)
            return
        self.loaded.append(str(path))
        level = None
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^#\s*第\s*(\d+)\s*级", line)
            if m:
                level = int(m.group(1))
                continue
            m = re.match(r"^\*\*([^*\n]+?)\*\*(.*)$", line)
            if not m:
                continue
            head, rest = m.group(1).strip(), m.group(2)
            if CJK.search(head) or "`" in head or not HEAD_OK.match(nfd(head)):
                continue
            g = re.search(r"【([^】]*)】", rest)
            self._add(head, level if graded else None, src, rest.strip(), g.group(1) if g else "")

    def _load_ledger(self, path: Path):
        if not path.exists():
            return
        self.loaded.append(str(path))
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*✧\s*`([^`]+)`\s*\|(.*)$", line)
            if m:
                cells = [c.strip() for c in m.group(2).split("|")]
                self._add(m.group(1), None, "词账✧", " | ".join(cells))
                self.coined[key(m.group(1))] = {"src": "词账✧"}
                continue
            m = re.match(r"^\|\s*\*\*第\s*(\d+)\s*级\*\*\s*\|", line)
            if m:  # 回补候选表：37 枚在册但未进本地词典正文
                lv = int(m.group(1))
                for f in re.findall(r"`([^`]+)`", line):
                    if key(f) not in self.entries:
                        self._add(f, lv, "词账·回补", "（37 枚回补之一；词典正文未收，释义见主书/词账）")

    def _load_coin_list(self, path: Path):
        if not path.exists():
            return
        self.loaded.append(str(path))
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*✧\s*`([^`]+)`\s*\|(.*)$", line)
            if m:
                cells = [c.strip() for c in m.group(2).split("|")]
                gloss = cells[1] if len(cells) > 1 else ""
                self.coined[key(m.group(1))] = {"src": "新铸词列表", "gloss": gloss, "cells": cells}
                self._add(m.group(1), None, "新铸词列表✧", " | ".join(cells), gloss)

    # -- 判定 -------------------------------------------------------
    def known(self, form):
        return key(form) in self.entries

    def variants(self, form):
        return sorted(self.by_base.get(base(key(form)), set()))


# ---------------------------------------------------------------- lookup
def cmd_lookup(args):
    lex = Lex(resolve_root(args.root))
    for q in args.query:
        print(f"== {q}")
        hits = []
        if CJK.search(q):
            for k, es in lex.entries.items():
                for e in es:
                    if q == e["gloss"]:
                        hits.append((0, e))
                    elif q in e["gloss"]:
                        hits.append((1, e))
                    elif q in e["text"]:
                        hits.append((2, e))
        else:
            qk, qb = key(q), base(key(q))
            for k, es in lex.entries.items():
                for e in es:
                    if k == qk:
                        hits.append((0, e))
                    elif base(k) == qb:
                        hits.append((1, e))
                    elif qb and qb in base(k):
                        hits.append((2, e))
        hits.sort(key=lambda t: (t[0], t[1]["level"] or 99))
        seen, n = set(), 0
        for _, e in hits:
            sig = (e["form"], e["src"], e["text"][:40])
            if sig in seen:
                continue
            seen.add(sig)
            lv = f"L{e['level']}" if e["level"] else "  "
            t = e["text"].replace("\n", " ")
            print(f"  [{lv:>3}|{e['src']}] {e['form']}  {t[:args.width]}")
            n += 1
            if n >= args.limit:
                print(f"  …（已截断，共 ≥{len(hits)} 条；加 --limit 看更多）")
                break
        if not hits:
            print("  （无）——若要用，须走铸词流程；先确认不是别的词形/汉义可达。")


# ---------------------------------------------------------------- check
def is_clitic(lex: Lex, part: str) -> bool:
    k = key(part)
    return k in CLITIC_ZERO or base(k) in CLITIC_BASES or ("-" + k) in lex.entries


def classify_part(lex: Lex, part: str, idx: int, attached: bool):
    """返回 (状态, 说明)。状态: ok / coined / variant / unknown"""
    k = key(part)
    if k in lex.entries or (k + "-") in lex.entries or ("-" + k) in lex.entries:
        return "ok", ""
    if k in lex.coined or (k + "-") in lex.coined:
        return "coined", ""
    if k in FREE_ZERO:
        return "ok", ""
    if (idx > 0 or attached) and (k in CLITIC_ZERO or base(k) in CLITIC_BASES):
        return "ok", ""
    vs = lex.variants(part)
    if vs:
        return "variant", "同骨架在册：" + "、".join(vs[:8])
    # 带前缀骨架的 -X 形（如 -nə́m）
    if base(k) in CLITIC_BASES:
        return "ok", ""
    return "unknown", ""


def cmd_check(args):
    root = resolve_root(args.root)
    lex = Lex(root)
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    problems, new_compounds, variants, coined_used = [], [], [], {}
    content_tokens = 0
    for ln, line in enumerate(text.splitlines(), 1):
        # 去掉 〔〕 注记与汉字
        clean = nfd(re.sub(r"〔[^〕]*〕", " ", line))
        for m in TOKEN.finditer(clean):
            tok = m.group(0)
            if tok.strip("-:'") == "":
                continue
            if re.fullmatch(r"[A-Z]{1,3}", tok):  # 变量 A B
                continue
            attached = tok.startswith("-")
            core = tok.strip("-")
            if not core:
                continue
            parts = [p for p in core.split("-") if p]
            content_tokens += 1
            # 结构：每个连字符段恰一个韵核
            for p in parts:
                vg = vowel_groups(p)
                if vg != 1 and not re.fullmatch(r"[ʔ…]*", p):
                    problems.append((ln, tok, f"段 `{p}` 含 {vg} 个韵核：疑似多音节未加连字符"))
            whole = key(core)
            if whole in lex.entries:
                continue
            if whole in lex.coined:
                coined_used[whole] = ln
                continue
            # 剥掉词尾的附着成分（循格、判据、复数、过程小词…）：它们是能产的，不算新词
            stem = list(parts)
            while len(stem) > 1 and is_clitic(lex, stem[-1]):
                stem.pop()
            skey = key("-".join(stem))
            if len(stem) < len(parts) and (skey in lex.entries or skey in lex.coined):
                if skey in lex.coined:
                    coined_used[skey] = ln
                continue
            statuses = [classify_part(lex, p, i, attached) for i, p in enumerate(stem)]
            kinds = [s for s, _ in statuses]
            if len(stem) == 1:
                s, note = statuses[0]
                if s == "ok":
                    continue
                if s == "coined":
                    coined_used[whole] = ln
                elif s == "variant":
                    variants.append((ln, tok, note))
                else:
                    problems.append((ln, tok, "未登记：词典/词账/新铸词列表都没有"))
            else:
                if "unknown" in kinds:
                    bad = [p for p, (s, _) in zip(stem, statuses) if s == "unknown"]
                    problems.append((ln, tok, "素未登记：" + "、".join(f"`{b}`" for b in bad)))
                elif "variant" in kinds:
                    for p, (s, n) in zip(stem, statuses):
                        if s == "variant":
                            variants.append((ln, f"{tok} 中的 {p}", n))
                else:
                    new_compounds.append((ln, "-".join(stem) + (("  〔+附着 " + "-".join(parts[len(stem):]) + "〕") if len(stem) < len(parts) else "")))
    print(f"档案根：{root}")
    print(f"已载入：{len(lex.entries)} 个词头；校验词符 {content_tokens} 个\n")
    def block(title, rows, fmt):
        print(f"{title}（{len(rows)}）")
        for r in rows:
            print("  " + fmt(r))
        if not rows:
            print("  无")
        print()
    block("✗ 必须处理", problems, lambda r: f"L{r[0]}  {r[1]}  —  {r[2]}")
    seen, uniq = set(), []
    for r in new_compounds:
        if r[1] not in seen:
            seen.add(r[1]); uniq.append(r)
    block("◇ 复合词，各素在册、整体未登记（待判：命名新概念/专名 → coin 登记；当场的透明限定复合 → 不必另立账）", uniq, lambda r: f"L{r[0]}  {r[1]}")
    block("△ 变调/变形：骨架在册，需人工核该调形是否真实可用", variants, lambda r: f"L{r[0]}  {r[1]}  —  {r[2]}")
    print(f"✧ 已登记临时词在本稿中出现：{len(coined_used)} 枚" + ("：" + "、".join(coined_used) if coined_used else ""))
    if content_tokens:
        ratio = 100 * (len(coined_used) + len(uniq)) / content_tokens
        flag = "  ← 超过 5%，须重配弯，少铸" if ratio > 5 else ""
        print(f"临时词占词符：≤{ratio:.1f}%（上限估计，含待判复合；健康线 5%）{flag}")
    print("\n注：本脚本只核词形与一格一音节；座架位置、否定位置、判据辖域、事化等语法须人工对照词法手册。")


# ---------------------------------------------------------------- coin
COIN_HEAD = """# 新铸词列表

**译写过程中产生的 ✧ 临时词。** 不是词典：进不了词典、词表、考级。规矩同《临时词账》：

1. **铸之前先查**（`nakthu_lex.py lookup`）：词典、分级词典、词账、本列表。撞形即并，不许同一个形两个义。
2. **级由形算出**：四个槽逐一读，取最晚那一项资源的级。
3. **「例句不够」与「语言缺词」是两件事**：真缺的标 ✦ 候选，另交词典编委，不在此账停留。
4. 过铸词四关：格点核查（骨架空）· 不添新簇 · 年代落位 · 听感回避。

| ✧形 | 构成（逐槽或构拟） | 义 | 类 | 级 | 首见（篇目·日期） |
|---|---|---|---|---|---|
"""


def cmd_coin(args):
    root = resolve_root(args.root)
    lex = Lex(root)
    form = args.form.strip()
    k = key(form)
    path = root / COIN_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    # 撞形检查
    if k in lex.entries and k not in lex.coined and not args.force:
        es = lex.entries[k]
        sys.exit(f"✗ `{form}` 已在册（{es[0]['src']}）：{es[0]['text'][:80]}\n  不得重铸；若义不同，换一个形。")
    if k in lex.coined and lex.coined[k].get("src") == "词账✧" and not args.force:
        sys.exit(f"✗ `{form}` 已在《临时词账》✧：同形请直接沿用，不要在此重登记（加 --force 可强登）。")
    vs = [v for v in lex.variants(form) if key(v) != k]
    if vs:
        print(f"△ 同骨架（仅调不同）在册：{'、'.join(vs[:8])}——请确认这一调形不撞既有义。")
    stamp = _dt.date.today().isoformat()
    first = f"{args.source}·{stamp}" if args.source else stamp
    row = f"| ✧ `{form}` | {args.slots} | {args.gloss} | {args.kind} | {args.level} | {first} |"
    if not path.exists():
        path.write_text(COIN_HEAD, encoding="utf-8", newline="\n")
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\|\s*✧\s*`([^`]+)`\s*\|(.*)$", line)
        if m and key(m.group(1)) == k:
            cells = [c.strip() for c in m.group(2).split("|") if c.strip() != ""]
            old_gloss = cells[1] if len(cells) > 1 else ""
            if old_gloss != args.gloss:
                sys.exit(f"✗ 撞形而两义：`{form}` 已登记为「{old_gloss}」，现拟「{args.gloss}」。换形，或确认同义。")
            if args.source and args.source not in line:
                lines[i] = line.rstrip(" |") + f"；{first} |"
                path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
                print(f"= `{form}` 已登记，同义；已追加首见：{first}")
            else:
                print(f"= `{form}` 已登记，同义，无需改动。")
            return
    raw = path.read_text(encoding="utf-8")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        if raw and not raw.endswith("\n"):
            fh.write("\n")
        fh.write(row + "\n")
    print(f"+ 已登记 ✧ `{form}` → {path}")


# ---------------------------------------------------------------- where
def cmd_where(args):
    root = resolve_root(args.root)
    lang = root / "language"
    print(f"档案根：{root}")
    for rel in (GRADED, DICT, LEDGER, "梦天语（Nakthu）：一门旨在加速人类进步的造语.md",
                "梦天语（Nakthu）文学与翻译汇编【上册】.md", "梦天语文体示例集.md",
                Path("_grammar_book") / "梦天语词法手册.md"):
        p = lang / rel
        print(f"  {'✓' if p.exists() else '✗'} {p}")
    cp = root / COIN_REL
    print(f"  新铸词列表：{cp}  {'（已存在）' if cp.exists() else '（尚未创建）'}")


def main():
    ap = argparse.ArgumentParser(description="梦天语译写辅助")
    ap.add_argument("--root", help="档案根目录（含 language\\）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("where").set_defaults(fn=cmd_where)
    p = sub.add_parser("lookup")
    p.add_argument("query", nargs="+")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--width", type=int, default=150)
    p.set_defaults(fn=cmd_lookup)
    p = sub.add_parser("check")
    p.add_argument("file", help="含梦天语转写的文件；- 表示 stdin")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("coin")
    p.add_argument("--form", required=True)
    p.add_argument("--slots", required=True, help="构成：复合写“素＋素”，新形逐槽写“起首＋韵核＋韵尾＋调”")
    p.add_argument("--gloss", required=True, help="义（简短）")
    p.add_argument("--kind", default="复合", help="复合 / 专名 / 变调 / 变核 / 声训新形")
    p.add_argument("--level", type=int, required=True, help="级(0-10)，由形算出")
    p.add_argument("--source", default="", help="首见篇目")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_coin)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
