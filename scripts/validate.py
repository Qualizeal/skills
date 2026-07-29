#!/usr/bin/env python3
"""Structural validation for the qz-agent-clusters marketplace.

Runs without auth or network, so it works in any CI runner. Complements
`claude plugin validate .`, which checks the official schema.
"""
import glob, json, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

errors, warnings = [], []


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        errors.append(f"{path}: no YAML frontmatter")
        return {}
    try:
        return yaml.safe_load(text[4:text.index("\n---\n", 3)]) or {}
    except Exception as exc:
        errors.append(f"{path}: frontmatter failed to parse — {exc}")
        return {}


# --- marketplace manifest -------------------------------------------------
mpath = ".claude-plugin/marketplace.json"
if not os.path.exists(mpath):
    sys.exit(f"missing {mpath}")
mk = json.load(open(mpath, encoding="utf-8"))

for field in ("name", "owner", "plugins"):
    if field not in mk:
        errors.append(f"marketplace.json: missing required field '{field}'")

RESERVED = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
    "claude-plugins-community", "claude-community", "anthropic-marketplace",
    "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
    "knowledge-work-plugins", "life-sciences", "claude-for-legal",
    "claude-for-financial-services", "financial-services-plugins",
    "first-party-plugins", "healthcare",
}
if mk.get("name") in RESERVED:
    errors.append(f"marketplace name '{mk['name']}' is reserved by Anthropic")
if not re.fullmatch(r"[a-z0-9-]+", mk.get("name", "")):
    errors.append("marketplace name must be kebab-case")

# Shared-root layout: no plugin.json may exist anywhere.
stray = glob.glob("**/plugin.json", recursive=True)
if stray:
    errors.append(
        "plugin.json found at " + ", ".join(stray)
        + " — conflicts with strict:false entries sharing source './'"
    )

seen = set()
claimed_skills, claimed_agents = set(), set()

for entry in mk.get("plugins", []):
    name = entry.get("name", "<unnamed>")
    if name in seen:
        errors.append(f"duplicate plugin name '{name}'")
    seen.add(name)
    if not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append(f"plugin name '{name}' is not kebab-case (claude.ai sync rejects these)")
    if entry.get("source") == "./":
        if entry.get("strict") is not False:
            errors.append(f"{name}: source './' requires \"strict\": false")
        if not entry.get("skills") or not entry.get("agents"):
            warnings.append(
                f"{name}: shared root without explicit skills/agents paths "
                "— this entry will load every cluster"
            )
    if len(entry.get("skills", [])) != 1 or len(entry.get("agents", [])) != 1:
        warnings.append(
            f"{name}: {len(entry.get('skills', []))} skills / {len(entry.get('agents', []))} agents "
            "— this marketplace pairs exactly one of each per plugin so capabilities install individually"
        )
    if not entry.get("description"):
        warnings.append(f"{name}: no description")
    if not entry.get("version"):
        warnings.append(f"{name}: no version — updates will track the commit SHA")
    # A `skills` path must point AT a directory containing SKILL.md — not at a
    # parent folder of skill directories. Getting this wrong loads one broken
    # entry instead of the whole cluster, silently.
    for path in entry.get("skills", []):
        if ".." in path:
            errors.append(f"{name}: path '{path}' escapes the marketplace root")
        elif not os.path.isdir(path):
            errors.append(f"{name}: skills path '{path}' does not exist")
        elif not os.path.isfile(os.path.join(path, "SKILL.md")):
            nested = glob.glob(os.path.join(path, "*", "SKILL.md"))
            errors.append(
                f"{name}: skills path '{path}' has no SKILL.md directly inside it"
                + (f" — it contains {len(nested)} skill dirs; list each one separately"
                   if nested else "")
            )
        else:
            claimed_skills.add(os.path.normpath(path))

    for path in entry.get("agents", []):
        if ".." in path:
            errors.append(f"{name}: path '{path}' escapes the marketplace root")
        elif os.path.isfile(path):
            claimed_agents.add(os.path.normpath(path))
        elif os.path.isdir(path):
            for f in glob.glob(os.path.join(path, "*.md")):
                claimed_agents.add(os.path.normpath(f))
        else:
            errors.append(f"{name}: agents path '{path}' does not exist")

# --- agents ---------------------------------------------------------------
agents = sorted(glob.glob("agents/*/*.md"))
for path in agents:
    data = frontmatter(path)
    stem = os.path.basename(path)[:-3]
    if data.get("name") != stem:
        errors.append(f"{path}: frontmatter name '{data.get('name')}' != filename '{stem}'")
    if not re.fullmatch(r"[a-z0-9-]+", str(data.get("name", ""))):
        errors.append(f"{path}: agent name must be kebab-case")
    desc = data.get("description", "")
    if len(desc) < 40:
        warnings.append(f"{path}: thin description — Claude delegates on this field")
    if data.get("model") not in (None, "sonnet", "opus", "haiku", "inherit"):
        errors.append(f"{path}: invalid model '{data.get('model')}'")
    if os.path.normpath(path) not in claimed_agents:
        errors.append(f"{path}: not claimed by any marketplace entry — will not load")

# --- skills ---------------------------------------------------------------
skills = sorted(glob.glob("skills/*/*/SKILL.md"))
for path in skills:
    data = frontmatter(path)
    parent = os.path.basename(os.path.dirname(path))
    if data.get("name") != parent:
        errors.append(f"{path}: frontmatter name '{data.get('name')}' != directory '{parent}'")
    if len(data.get("description", "")) < 40:
        warnings.append(f"{path}: thin description — Claude loads skills on this field")

for orphan in glob.glob("skills/*/*"):
    if os.path.isdir(orphan) and not os.path.exists(os.path.join(orphan, "SKILL.md")):
        errors.append(f"{orphan}: skill directory without SKILL.md")

for path in skills:
    d = os.path.normpath(os.path.dirname(path))
    if d not in claimed_skills:
        errors.append(f"{d}: skill not claimed by any marketplace entry — will not load")

# --- report ---------------------------------------------------------------
for w in warnings:
    print(f"WARN  {w}")
for e in errors:
    print(f"ERROR {e}")
print(f"\n{mk.get('name')}: {len(mk.get('plugins', []))} entries, "
      f"{len(agents)} agents, {len(skills)} skills")
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
