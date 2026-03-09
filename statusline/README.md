# Claude Code Custom Statusline

A custom statusline script for Claude Code that displays the current model, working directory, git branch, and a context window usage bar.

Example output:

```
[Claude 4.6 Opus] 📁 my-project |⚡️ main | [████████░░░░░░░░░░░░] 40.0% (67K/167K)
```

## What it shows

- **Model** — the active Claude model
- **Directory** — current working directory name
- **Git branch** — current branch (if inside a git repo)
- **Context usage** — a progress bar with percentage and token counts, scaled to the effective limit (167K with auto-compact on, 200K with it off)

## Setup

1. Copy `statusline-command.py` somewhere on your machine (e.g. `~/.claude/statusline-command.py`):

   ```sh
   cp statusline/statusline-command.py ~/.claude/statusline-command.py
   ```

2. Make sure it's executable:

   ```sh
   chmod +x ~/.claude/statusline-command.py
   ```

3. Open your Claude Code settings file at `~/.claude/settings.json` and add the `statusCommand` field:

   ```json
   {
     "statusCommand": "python3 ~/.claude/statusline-command.py"
   }
   ```

   If the file doesn't exist, create it with just that content.

4. Restart Claude Code. The custom statusline should now appear at the bottom of your terminal.

## Requirements

- Python 3
- Claude Code CLI
