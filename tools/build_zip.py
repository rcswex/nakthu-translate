#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 skills/nakthu-translate/ 打成可上传到 Claude Chat（claude.ai / 桌面应用 Chat 标签）的 zip。

用法：python tools/build_zip.py [输出路径]      默认 dist/nakthu-translate.zip
zip 内顶层目录是 nakthu-translate/，其下即 SKILL.md、references/、scripts/、archive/。
条目名一律用正斜杠、UTF-8，跨平台可读。
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills" / "nakthu-translate"
SKIP_DIRS = {"__pycache__", ".git"}
SKIP_SUFFIX = {".pyc"}


CHAT_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def strip_frontmatter(text: str) -> str:
    """只保留 Chat 认的 frontmatter 键；其余（如 argument-hint）去掉。"""
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        return text
    kept, dropped = [], []
    for line in parts[1].strip("\n").splitlines():
        k = line.split(":", 1)[0].strip()
        if line[:1] in (" ", "\t") or k in CHAT_KEYS:
            kept.append(line)
        else:
            dropped.append(k)
    if dropped:
        print("zip 内 SKILL.md 已去掉 frontmatter 键：" + "、".join(dropped))
    return "---\n" + "\n".join(kept) + "\n---" + parts[2]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist" / "nakthu-translate.zip"
    if not (SRC / "SKILL.md").exists():
        sys.exit(f"找不到 {SRC / 'SKILL.md'}")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Chat 上传会拒绝含非 ASCII 字符的 zip 路径（"path with invalid characters"），先检查
    bad = [p.relative_to(SRC).as_posix() for p in SRC.rglob("*")
           if not SKIP_DIRS & set(p.relative_to(SRC).parts) and not p.relative_to(SRC).as_posix().isascii()]
    if bad:
        sys.exit("以下路径含非 ASCII 字符，Chat 上传会被拒绝，请改成 ASCII 名：\n  " + "\n  ".join(bad))
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(SRC.rglob("*")):
            if p.is_dir() or SKIP_DIRS & set(p.relative_to(SRC).parts) or p.suffix in SKIP_SUFFIX:
                continue
            arc = "nakthu-translate/" + p.relative_to(SRC).as_posix()
            if arc == "nakthu-translate/SKILL.md":
                # Chat 的 skill 校验只认少数 frontmatter 键；Claude Code 专用的键（如 argument-hint）
                # 会让上传被拒或被忽略，所以只在 zip 里去掉，仓库里的 SKILL.md 不变。
                z.writestr(arc, strip_frontmatter(p.read_text(encoding="utf-8")))
            else:
                z.write(p, arc)
            n += 1
    print(f"已生成 {out}  （{n} 个文件，{out.stat().st_size / 1024 / 1024:.1f} MB）")
    print("上传：Claude Chat → 设置 → 功能（Capabilities）→ Skills → 上传 skill；上传前先删掉旧版 nakthu-translate。")


if __name__ == "__main__":
    main()
