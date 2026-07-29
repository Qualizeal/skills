#!/usr/bin/env python3
"""Validate the qz-agent-clusters marketplace (standard plugin layout).

Each plugin is a self-contained directory under plugins/ with its own
.claude-plugin/plugin.json. Skills and agents are auto-discovered from
skills/<name>/SKILL.md and agents/<name>.md — there are no paths in
marketplace.json to get wrong.

    pip install pyyaml && python3 scripts/validate.py
"""
import glob, json, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

errors, warnings = [], []
RESERVED = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
    "claude-plugins-community", "claude-community", "anthropic-marketplace",
    "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
    "knowledge-work-plugins", "life-sciences", "claude-for-legal",
    "claude-for-financial-services", "financial-services-plugins",
    "first-party-plugins", "healthcare",
}


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    for line in text.split("\n")[:6]:
        if line.startswith("description: ") and not line[13:].lstrip().startswith(('"', "'")):
            if ": " in line[13:]:
                errors.append(f"{path}: unquoted description contains ': ' — wrap it in double quotes")
    if not text.startswith("---\n"):
        errors.append(f"{path}: no YAML frontmatter")
        return {}
    try:
        return yaml.safe_load(text[4:text.index("\n---\n", 3)]) or {}
    except Exception as exc:
        errors.append(f"{path}: frontmatter failed to parse — {exc}")
        return {}


mpath = ".claude-plugin/marketplace.json"
if not os.path.exists(mpath):
    sys.exit(f"missing {mpath}")
mk = json.load(open(mpath, encoding="utf-8"))

for field in ("name", "owner", "plugins"):
    if field not in mk:
        errors.append(f"marketplace.json: missing required field '{field}'")
if mk.get("name") in RESERVED:
    errors.append(f"marketplace name '{mk['name']}' is reserved by Anthropic")
if not re.fullmatch(r"[a-z0-9-]+", mk.get("name", "")):
    errors.append("marketplace name must be kebab-case")

seen, listed_dirs = set(), set()
total_skills = total_agents = 0

for entry in mk.get("plugins", []):
    name = entry.get("name", "<unnamed>")
    if name in seen:
        errors.append(f"duplicate plugin name '{name}'")
    seen.add(name)
    if not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append(f"plugin name '{name}' is not kebab-case")

    src = entry.get("source")
    if not isinstance(src, str) or not src.startswith("./"):
        errors.append(f"{name}: source must be a relative path to its plugin directory")
        continue
    if ".." in src:
        errors.append(f"{name}: source '{src}' escapes the marketplace root")
        continue
    if not os.path.isdir(src):
        errors.append(f"{name}: source directory '{src}' does not exist")
        continue
    listed_dirs.add(os.path.normpath(src))

    # the plugin's own manifest is the authority here
    pj = os.path.join(src, ".claude-plugin", "plugin.json")
    if not os.path.isfile(pj):
        errors.append(f"{name}: missing {pj}")
    else:
        try:
            man = json.load(open(pj, encoding="utf-8"))
            if man.get("version") and entry.get("version") and man["version"] != entry["version"]:
                errors.append(f"{name}: plugin.json version {man['version']} != marketplace entry {entry['version']}")
            if man.get("name") != name:
                errors.append(f"{name}: plugin.json name '{man.get('name')}' does not match the marketplace entry")
            if not man.get("version"):
                warnings.append(f"{name}: plugin.json has no version — updates will track the commit SHA")

            # Explicit arrays must list every skill and agent on disk. Tools that
            # read the manifest rather than walking folders show only what is listed.
            declared = set(man.get("skills") or [])
            actual = {"./skills/" + os.path.basename(os.path.dirname(s))
                      for s in glob.glob(os.path.join(src, "skills", "*", "SKILL.md"))}
            if not declared:
                errors.append(f"{name}: plugin.json has no 'skills' array — viewers that read the manifest will show none")
            for missing in sorted(actual - declared):
                errors.append(f"{name}: skill '{missing}' exists on disk but is not in plugin.json's skills array")
            for phantom in sorted(declared - actual):
                errors.append(f"{name}: plugin.json lists '{phantom}' but no SKILL.md is there")

            dec_a = set(man.get("agents") or [])
            act_a = {"./agents/" + os.path.basename(a) for a in glob.glob(os.path.join(src, "agents", "*.md"))}
            for missing in sorted(act_a - dec_a):
                errors.append(f"{name}: agent '{missing}' exists on disk but is not in plugin.json's agents array")
            for phantom in sorted(dec_a - act_a):
                errors.append(f"{name}: plugin.json lists '{phantom}' but the file is missing")
        except Exception as exc:
            errors.append(f"{pj}: invalid JSON — {exc}")

    # The marketplace entry must be self-describing: some viewers read only this
    # level and fall back to a default version and a skill count of 1 without it.
    if not entry.get("version"):
        errors.append(f"{name}: marketplace entry has no 'version' — viewers fall back to a default")
    actual_entry = {"./skills/" + os.path.basename(os.path.dirname(s))
                    for s in glob.glob(os.path.join(src, "skills", "*", "SKILL.md"))}
    declared_entry = set(entry.get("skills") or [])
    if not declared_entry:
        errors.append(f"{name}: marketplace entry has no 'skills' array — viewers show one placeholder skill")
    elif declared_entry != actual_entry:
        for m in sorted(actual_entry - declared_entry):
            errors.append(f"{name}: entry skills array missing '{m}'")
        for m in sorted(declared_entry - actual_entry):
            errors.append(f"{name}: entry skills array lists '{m}' which does not exist")
    if not entry.get("agents"):
        warnings.append(f"{name}: marketplace entry has no 'agents' array")

    skills = sorted(glob.glob(os.path.join(src, "skills", "*", "SKILL.md")))
    agents = sorted(glob.glob(os.path.join(src, "agents", "*.md")))
    total_skills += len(skills)
    total_agents += len(agents)

    if not skills:
        errors.append(f"{name}: no skills found at {src}/skills/<name>/SKILL.md")
    if not agents:
        warnings.append(f"{name}: no agents found at {src}/agents/*.md")

    for s in skills:
        d = frontmatter(s)
        parent = os.path.basename(os.path.dirname(s))
        if d.get("name") != parent:
            errors.append(f"{s}: frontmatter name '{d.get('name')}' != directory '{parent}'")
        if len(str(d.get("description", ""))) < 40:
            warnings.append(f"{s}: thin description — Claude loads skills on this field")

    for a in agents:
        d = frontmatter(a)
        stem = os.path.basename(a)[:-3]
        if d.get("name") != stem:
            errors.append(f"{a}: frontmatter name '{d.get('name')}' != filename '{stem}'")
        if d.get("model") not in (None, "sonnet", "opus", "haiku", "inherit"):
            errors.append(f"{a}: invalid model '{d.get('model')}'")

    for extra in os.listdir(src):
        if extra not in (".claude-plugin", "skills", "agents", "commands", "hooks",
                         "README.md", "LICENSE", ".mcp.json"):
            warnings.append(f"{name}: unexpected entry '{extra}' in the plugin directory")

# every plugin directory on disk must be listed
for d in sorted(glob.glob("plugins/*")):
    if os.path.isdir(d) and os.path.normpath(d) not in listed_dirs:
        errors.append(f"{d}: plugin directory not listed in marketplace.json — it will never install")

# an empty skill folder loads nothing
for d, subdirs, files in os.walk("plugins"):
    if os.path.basename(os.path.dirname(d)) == "skills" and "SKILL.md" not in files and not subdirs:
        errors.append(f"{d}: skill directory without SKILL.md")

for w in warnings:
    print(f"WARN  {w}")
for e in errors:
    print(f"ERROR {e}")
print(f"\n{mk.get('name')} v{mk.get('version','?')}: {len(mk.get('plugins', []))} plugins, "
      f"{total_skills} skills, {total_agents} agents")
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
