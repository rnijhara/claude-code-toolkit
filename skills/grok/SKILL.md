---
name: grok
description: >
  Query Grok (xAI) with native X/Twitter search access. Use this skill whenever the user
  wants to fetch a specific tweet or X thread by URL, search X/Twitter for posts or discussions
  on a topic, check reactions or discourse on X, or any task where real-time X/Twitter data
  would be useful. Triggers on: X/Twitter URLs (x.com links, twitter.com links), "check X for",
  "what's the reaction on X/Twitter", "fetch this tweet", "search X for", "from:handle",
  or any request involving real-time social media content from X/Twitter. Also use when the
  user pastes an x.com or twitter.com URL and wants to know what it says.
---

# Grok: X/Twitter Search via xAI

This skill calls xAI's Grok API with the `x_search` tool, giving you native access to X/Twitter data. Grok can fetch specific tweets, search for discussions, and answer questions using real-time X content.

## How to use

Take the user's prompt (or URL) and pass it to the bundled script. The script handles the API call and returns Grok's raw response.

### Running the script

The script is at `scripts/grok.py` within this skill's directory. Resolve the path relative to where you loaded this SKILL.md file.

```bash
python3 scripts/grok.py "<user's prompt or question>"
```

The script reads `XAI_API_KEY` from `~/.config/grok/.env` (or from the shell environment). `XAI_MODEL` is optional, defaults to `grok-4-1-fast-non-reasoning`.

### Setup

The API key must be configured at `~/.config/grok/.env`:

```
XAI_API_KEY=xai-your-key-here
XAI_MODEL=grok-4-1-fast-non-reasoning   # optional
```

If the key is missing, the script prints setup instructions. Pass these to the user so they can configure it.

### What to pass as the prompt

Pass the user's input directly, but adjust framing slightly depending on what they need:

**Fetching a specific tweet/thread:** If the user gives an X URL, ask Grok to return the full text.
```bash
python3 scripts/grok.py "Find and return the FULL untruncated text of this tweet: https://x.com/user/status/123. Include the complete thread if it's part of one."
```

**Searching for posts:** Pass the search query naturally.
```bash
python3 scripts/grok.py "Search X for discussions about MSA Memory Sparse Attention in the last week. Return the most relevant posts with author handles, dates, and engagement."
```

**Open-ended questions:** Just pass the question through.
```bash
python3 scripts/grok.py "What's the reaction on X to the new DeepSeek V4 release today?"
```

### Output

The script prints Grok's raw text response. Present this directly to the user without additional summarization or reformatting, unless they ask you to process it further. The value of this skill is giving the user access to what Grok found, not your interpretation of it.

### Error handling

If `XAI_API_KEY` is not set, the script returns a clear error message. Let the user know they need to set it in their environment or Claude Code settings.

### Tips for good results

- For tweet fetches, explicitly ask for "FULL untruncated text" since Grok may truncate long threads
- For searches, include a time range ("this week", "last 30 days") to get recent results
- X search operators work: `from:handle`, `to:handle`, date ranges
- For threads, ask Grok to "return all parts of the thread"
