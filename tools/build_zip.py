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


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist" / "nakthu-translate.zip"
    if not (SRC / "SKILL.md").exists():
        sys.exit(f"找不到 {SRC / 'SKILL.md'}")
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(SRC.rglob("*")):
            if p.is_dir() or SKIP_DIRS & set(p.relative_to(SRC).parts) or p.suffix in SKIP_SUFFIX:
                continue
            arc = "nakthu-translate/" + p.relative_to(SRC).as_posix()
            z.write(p, arc)
            n += 1
    print(f"已生成 {out}  （{n} 个文件，{out.stat().st_size / 1024 / 1024:.1f} MB）")
    print("上传：Claude Chat → 设置 → 功能（Capabilities）→ Skills → 上传 skill；上传前先删掉旧版 nakthu-translate。")


if __name__ == "__main__":
    main()
