#!/usr/bin/env python3
"""
Custom statusline for Claude Code.

Reads the model's context window size from stdin JSON
(context_window.context_window_size) and respects the CLAUDE_CODE_AUTO_COMPACT_WINDOW
env var when set, capped at the model's actual window (env var can shrink but
not grow beyond what the model supports).

Auto-compact reserves a fixed 33K token buffer (e.g. 167K effective for a 200K
window, 967K for 1M). The percentage and bar scale to whichever limit is active.

The model segment includes the effort level (effort.level) when present.

The rate-limit segment shows the 5-hour (session) and 7-day (weekly) usage
percentages from rate_limits, followed by session cost.

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
effort_level = (data.get("effort") or {}).get("level")
if effort_level:
    model = f"{model} \u00b7 {effort_level}"
current_dir = os.path.basename(data["workspace"]["current_dir"])

git_branch = ""
project_dir = data.get("workspace", {}).get("project_dir", "")
git_head_path = os.path.join(project_dir, ".git", "HEAD")
if os.path.exists(git_head_path):
    try:
        with open(git_head_path, "r") as f:
            ref = f.read().strip()
            if ref.startswith("ref: refs/heads/"):
                git_branch = f" | ⚡️ {ref.replace('ref: refs/heads/', '')}"
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

try:
    compact_window_env = int(os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW", "0"))
except ValueError:
    compact_window_env = 0
compact_window = min(compact_window_env, context_window_size) if compact_window_env > 0 else context_window_size

autocompact_threshold = max(compact_window - AUTOCOMPACT_BUFFER, 0)
effective_limit = autocompact_threshold if auto_compact_on else compact_window
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

LIMIT_SEPARATOR = " \u00b7 "
rate_limits = data.get("rate_limits", {})
limit_parts = []
for key, label in (("five_hour", "5h"), ("seven_day", "7d")):
    window = rate_limits.get(key)
    if not window:
        continue
    limit_parts.append(f"{label} {window.get('used_percentage', 0):.0f}%")
limits_display = f" | \U0001f50b {LIMIT_SEPARATOR.join(limit_parts)}" if limit_parts else ""

session_cost = data.get("cost", {}).get("total_cost_usd")
cost_display = f" | \U0001f4b0 ${session_cost:.2f}" if session_cost is not None else ""

print(f"[{model}] \U0001f4c1 {current_dir}{git_branch}{context_usage}{limits_display}{cost_display}")
