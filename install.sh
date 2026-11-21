#!/usr/bin/env sh
# Install the nakthu-translate skill for Claude Code (user level).
# Usage: sh install.sh [target-skills-dir]
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-$HOME/.claude/skills}"
mkdir -p "$TARGET"
rm -rf "$TARGET/nakthu-translate"
cp -R "$HERE/skills/nakthu-translate" "$TARGET/nakthu-translate"
find "$TARGET/nakthu-translate" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "Installed to $TARGET/nakthu-translate"
echo "The Nakthu archive snapshot is bundled (archive/); no other setup needed."
echo "Optional: set NAKTHU_ROOT to a live archive (the directory containing language/)."
