# VS Code Agent Plugins (Preview)

The Extensions-sidebar view titled **Agent Plugins: Marketplace** is a VS Code feature, not Claude Code. Its manifest rules differ in one field that matters here.

## The field that breaks it

VS Code's `plugin.json` reference:

> `skills` — Path(s) to skill directories. **Defaults to `skills/`.**

That is the *container* directory. Its own example is:

```json
{
  "name": "my-dev-tools",
  "version": "1.2.0",
  "skills": "skills/",
  "agents": "agents/"
}
```

Listing each individual skill directory instead — `["./skills/artefact-ingestion", "./skills/redaction-policy", ...]` — makes VS Code treat every entry as a container, look inside for `*/SKILL.md`, find nothing, and render a single placeholder. That is the "Skills 1" symptom.

Every `plugin.json` here now uses the container form.

## Register the marketplace

VS Code does not read Claude Code's marketplace registrations. Add it in `settings.json`:

```json
"chat.plugins.marketplaces": [
  "Qualizeal/skills"
]
```

Shorthand `owner/repo`, a full `.git` URL, an SSH remote, or a `file:///` path all work.

## Clear the cache when the version looks stuck

VS Code caches the cloned marketplace. On Windows:

```
%APPDATA%\Code\agentPlugins\github.com\Qualizeal\skills
```

macOS: `~/Library/Application Support/Code/agentPlugins/github.com/Qualizeal/skills`
Linux: `~/.config/Code/agentPlugins/github.com/Qualizeal/skills`

Delete that directory, then run **Extensions: Check for Extension Updates** from the Command Palette. VS Code also checks automatically every 24 hours, which is why a stale badge can persist for a long time.

## Requirements this repo already satisfies

- `plugin.json` is at `.claude-plugin/plugin.json`, one of the four recognised locations. VS Code probes `.plugin/plugin.json`, then `plugin.json`, then `.github/plugin/plugin.json`, then `.claude-plugin/plugin.json`.
- Every plugin `name` is plain kebab-case. Slashes, colons and namespace prefixes cause a silent load failure.
- Every skill directory name matches the `name` in its `SKILL.md` frontmatter. A mismatch makes the skill silently skipped. `scripts/validate.py` enforces this.
- `version` is set in both `plugin.json` and the marketplace entry, and bumped on every release, which is what drives the update check.

## Test locally before pushing

Point VS Code at the extracted folder rather than waiting on a push and a cache refresh:

```json
"chat.pluginLocations": {
  "D:/Downloads/qz-agent-clusters/plugins/qa-knowledge-fabric": true
}
```

Five skills should appear immediately. That isolates a manifest problem from a caching or deployment one in about a minute.
