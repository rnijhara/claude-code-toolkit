# Claude Code Custom Statusline

A custom statusline script for Claude Code that displays the current model, working directory, git branch, a context window usage bar, rate-limit usage, and session cost.

Example output:

```
[Opus 5.5] 📁 my-project | ⚡️ main | [████░░░░░░░░░░░░░░░░] 21.2% (120K/567K) | 🔋 5h 23% · 7d 41% | 💰 $1.23
```

## What it shows

- **Model** — the active Claude model
- **Directory** — current working directory name
- **Git branch** — current branch (if inside a git repo)
- **Context usage** — a progress bar with percentage and token counts, scaled to the effective limit. The window comes from the model's actual context size, optionally shrunk by `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (it can't exceed the model's window). With auto-compact on, a fixed 33K buffer is reserved (e.g. 167K for 200K, 967K for 1M, 567K with `CLAUDE_CODE_AUTO_COMPACT_WINDOW=600000`)
- **Rate limits** — 5-hour (session) and 7-day (weekly) usage percentages, when available
- **Session cost** — total cost in USD for the current session

## Setup

1. Copy `statusline-command.py` somewhere on your machine (e.g. `~/.claude/statusline-command.py`):

   ```sh
   cp statusline/statusline-command.py ~/.claude/statusline-command.py
   ```

2. Make sure it's executable:

   ```sh
   chmod +x ~/.claude/statusline-command.py
   ```

3. Open your Claude Code settings file at `~/.claude/settings.json` and add the `statusLine` field:

   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "python3 ~/.claude/statusline-command.py"
     }
   }
   ```

   If the file doesn't exist, create it with just that content.

4. Restart Claude Code. The custom statusline should now appear at the bottom of your terminal.

## Requirements

- Python 3.9+
- Claude Code CLI
