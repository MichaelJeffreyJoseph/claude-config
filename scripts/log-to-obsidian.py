#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

OBSIDIAN_LOG_DIR = Path("/Users/mickey/servers/MyObsidian/Claude Logs")

def parse_transcript(transcript_path):
    tool_counts = defaultdict(int)
    files_modified = []
    first_user_message = ""

    if not transcript_path or not os.path.exists(transcript_path):
        return tool_counts, files_modified, first_user_message

    with open(transcript_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg = entry.get("message", {})
            role = msg.get("role", entry.get("type", ""))
            content = msg.get("content", [])

            if role == "user" and not first_user_message:
                if isinstance(content, str):
                    first_user_message = content[:300]
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            first_user_message = block.get("text", "")[:300]
                            break

            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "tool_use":
                        name = block.get("name", "unknown")
                        tool_counts[name] += 1
                        if name in ("Edit", "Write"):
                            fp = block.get("input", {}).get("file_path", "")
                            if fp and fp not in files_modified:
                                files_modified.append(fp)

    return tool_counts, files_modified, first_user_message


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    OBSIDIAN_LOG_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    short_id = session_id[:8]

    filename = OBSIDIAN_LOG_DIR / f"{date_str}_{short_id}.md"

    tool_counts, files_modified, first_user_message = parse_transcript(transcript_path)

    lines = [
        "---",
        f"date: {date_str}",
        f"session_id: {session_id}",
        "tags: [claude-session]",
        "---",
        "",
        f"# Claude Session — {date_str} {time_str}",
        "",
    ]

    if first_user_message:
        lines += [
            "## First Message",
            "",
            f"> {first_user_message.strip()}",
            "",
        ]

    if tool_counts:
        lines += ["## Tools Used", ""]
        for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
            lines.append(f"- **{tool}**: {count}")
        lines.append("")

    if files_modified:
        lines += ["## Files Modified", ""]
        for fp in files_modified:
            lines.append(f"- `{fp}`")
        lines.append("")

    lines += [
        "## Transcript",
        "",
        f"`{transcript_path}`",
        "",
    ]

    with open(filename, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
