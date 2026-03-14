#!/usr/bin/env python3
"""
Custom statusline for Claude Code.

Reads the model's actual context window size from stdin JSON
(context_window.context_window_size) instead of hardcoding 200K.
Auto-compact reserves a fixed 33K token buffer regardless of context window size
(e.g. 167K for 200K, 967K for 1M). The percentage and bar scale to whichever
limit is active.

Auto-compact is on when: autoCompactEnabled is true (default) in settings.json
AND neither DISABLE_COMPACT nor DISABLE_AUTO_COMPACT env vars are set.
"""
import json
import os
import sys

AUTOCOMPACT_BUFFER = 33000

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

context_window = data.get("context_window", {})
context_window_size = context_window.get("context_window_size", 200000)
autocompact_threshold = context_window_size - AUTOCOMPACT_BUFFER
effective_limit = autocompact_threshold if auto_compact_on else context_window_size
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
