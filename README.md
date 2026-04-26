# claude-config

Personal Claude Code configuration.

## Contents

| File | Live location |
|------|--------------|
| `settings.json` | `~/.claude/settings.json` |
| `claude_desktop_config.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| `scripts/log-to-obsidian.py` | Called by Stop hook on every session end |

## Setup on a new machine

```bash
git clone git@github.com:<you>/claude-config.git ~/claude-config

cp ~/claude-config/settings.json ~/.claude/settings.json
cp ~/claude-config/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## Syncing changes

Edit files in `~/claude-config/` directly, then copy to live locations:

```bash
cp ~/claude-config/settings.json ~/.claude/settings.json
```

## Obsidian logging

Each Claude Code session writes a log to `~/servers/MyObsidian/Claude Logs/`  
Format: `YYYY-MM-DD_<session-id>.md`  
Contains: first message, tools used, files modified, transcript path.
