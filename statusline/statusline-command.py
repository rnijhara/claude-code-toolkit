#!/usr/bin/env python3
"""
Custom statusline for Claude Code.

Detects whether auto-compact is enabled to show the effective context limit.
Auto-compact fires at 167K tokens (context_window 200K - 20K margin - 13K buffer).
When off, the full 200K is the ceiling. The percentage and bar scale to whichever
limit is active, and tokens are shown as e.g. "38K/167K" or "38K/200K".

Auto-compact is on when: autoCompactEnabled is true (default) in settings.json
AND neither DISABLE_COMPACT nor DISABLE_AUTO_COMPACT env vars are set.
"""
import json
import os
import sys

CONTEXT_WINDOW_SIZE = 200000
AUTOCOMPACT_THRESHOLD = 167000

SETTINGS_PATH = os.path.expanduser("~/.claude.json")

data = json.load(sys.stdin)

model = data["model"]["display_name"]
current_dir = os.path.basename(data["workspace"]["current_dir"])

git_branch = ""
project_dir = data.get("workspace", {}).get("project_dir", "")
git_head_path = os.path.join(project_dir, ".git", "HEAD")
if os.path.exists(git_head_path):
    try:
        with open(git_head_path, "r") as f:
            ref = f.read().strip()
            if ref.startswith("ref: refs/heads/"):
                git_branch = f" |⚡️ {ref.replace('ref: refs/heads/', '')}"
    except Exception:
        pass

auto_compact_on = True
try:
    with open(SETTINGS_PATH, "r") as f:
        settings = json.load(f)
    if settings.get("autoCompactEnabled") is False:
        auto_compact_on = False
except Exception:
    pass
if os.environ.get("DISABLE_COMPACT") or os.environ.get("DISABLE_AUTO_COMPACT"):
    auto_compact_on = False

effective_limit = AUTOCOMPACT_THRESHOLD if auto_compact_on else CONTEXT_WINDOW_SIZE

context_window = data.get("context_window", {})
current_usage = context_window.get("current_usage")

if current_usage:
    total_tokens = (
        current_usage.get("input_tokens", 0)
        + current_usage.get("cache_creation_input_tokens", 0)
        + current_usage.get("cache_read_input_tokens", 0)
        + current_usage.get("output_tokens", 0)
    )
else:
    total_tokens = 0

used_pct = min(total_tokens / effective_limit * 100, 100) if effective_limit > 0 else 0
tokens_k = f"{total_tokens // 1000}K"
limit_k = f"{effective_limit // 1000}K"

bar_length = 20
filled_length = int(bar_length * used_pct / 100)
bar = "█" * filled_length + "░" * (bar_length - filled_length)
context_usage = f" | [{bar}] {used_pct:.1f}% ({tokens_k}/{limit_k})"

print(f"[{model}] 📁 {current_dir}{git_branch}{context_usage}")
