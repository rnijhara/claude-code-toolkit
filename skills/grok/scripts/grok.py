"""Call xAI's Grok API with native X/Twitter search access.

Takes a user prompt as arguments, sends it to Grok via the xAI responses API
with the x_search tool enabled, and prints the raw response text.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

XAI_RESPONSES_URL = "https://api.x.ai/v1/responses"
MAX_RETRIES = 3
RETRY_DELAY = 2.0
DEFAULT_MODEL = "grok-4-1-fast-non-reasoning"
CONFIG_DIR = os.path.expanduser("~/.config/grok")
ENV_FILE = os.path.join(CONFIG_DIR, ".env")


def load_env():
    """Load variables from ~/.config/grok/.env if it exists."""
    if not os.path.isfile(ENV_FILE):
        return
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = value


def call_grok(prompt: str) -> str:
    load_env()

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        return (
            "Error: XAI_API_KEY not found.\n"
            f"Set it in {ENV_FILE}:\n"
            f"  mkdir -p {CONFIG_DIR}\n"
            f"  echo 'XAI_API_KEY=your-key-here' >> {ENV_FILE}"
        )

    model = os.environ.get("XAI_MODEL", DEFAULT_MODEL)

    payload = {
        "model": model,
        "tools": [{"type": "x_search"}],
        "input": [{"role": "user", "content": prompt}],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "grok-skill/1.0",
    }

    data = json.dumps(payload).encode("utf-8")

    last_error = None
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(XAI_RESPONSES_URL, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                response = json.loads(resp.read().decode("utf-8"))
            return extract_output(response)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            last_error = f"Error: xAI API returned {e.code}: {body}"
            if 400 <= e.code < 500 and e.code != 429:
                return last_error
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)
                time.sleep(delay)
        except Exception as e:
            return f"Error: {e}"

    return last_error


def extract_output(response: dict) -> str:
    """Extract the text output from xAI's response format."""
    if "error" in response and response["error"]:
        err = response["error"]
        msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
        return f"Error from xAI: {msg}"

    output = response.get("output", [])
    if isinstance(output, str):
        return output

    for item in output:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "message":
            for c in item.get("content", []):
                if isinstance(c, dict) and c.get("type") == "output_text":
                    return c.get("text", "")
        if "text" in item:
            return item["text"]

    # Fallback: check choices format
    for choice in response.get("choices", []):
        if "message" in choice:
            return choice["message"].get("content", "")

    return "No output returned from Grok."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: grok.py <prompt>")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    print(call_grok(prompt))
