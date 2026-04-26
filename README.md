# claude-config

Personal Claude Code configuration.

## Contents

| File | Live location |
|------|--------------|
| `settings.json` | `~/.claude/settings.json` |
| `settings.local.json` | `~/.claude/settings.local.json` |
| `claude_desktop_config.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| `scripts/log-to-obsidian.py` | Called by Stop hook on every session end |

## Setup on a new machine

```bash
git clone git@github.com:MichaelJeffreyJoseph/claude-config.git ~/claude-config

# Symlink settings so Claude Code writes directly into the repo
ln -s ~/claude-config/settings.json ~/.claude/settings.json
ln -s ~/claude-config/settings.local.json ~/.claude/settings.local.json

# Copy desktop config (Claude Desktop doesn't support symlinks here)
cp ~/claude-config/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## Syncing changes

`settings.json` and `settings.local.json` are symlinked — any change Claude Code makes is instantly reflected in this repo. Just commit when you want to snapshot:

```bash
cd ~/claude-config && git diff && git add -A && git commit -m "update settings" && git push
```

`claude_desktop_config.json` is a copy and must be manually synced if changed.

## Obsidian logging

Each Claude Code session writes a log to `~/servers/MyObsidian/Claude Logs/`  
Format: `YYYY-MM-DD_<session-id>.md`  
Contains: first message, tools used, files modified, transcript path.
