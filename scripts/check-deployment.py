#!/usr/bin/env python3
"""What is actually deployed, and which build is it?

    python3 scripts/check-deployment.py                  # this directory
    python3 scripts/check-deployment.py /path/to/repo

Build history:
    0.1.0   4 cluster plugins, shared root
    1.0.0   15 plugins, 1 skill each, shared root
    2.0.0   15 plugins, 67 skills, shared root + explicit skill paths
    3.0.0   15 self-contained plugin directories, skills auto-discovered
    3.1.0   plus explicit skills/agents arrays in each plugin.json
"""
import json, sys, os, glob

root = sys.argv[1] if len(sys.argv) > 1 else "."
path = os.path.join(root, ".claude-plugin", "marketplace.json")

if not os.path.isfile(path):
    sys.exit(f"No marketplace.json at {path}\n"
             "If you copied the folder in Explorer, the hidden .claude-plugin\n"
             "directory was probably skipped. That alone reverts the whole catalog.")

mk = json.load(open(path, encoding="utf-8"))
plugins = mk.get("plugins", [])
shared_root = any(p.get("source") == "./" for p in plugins)

print(f"marketplace : {mk.get('name')}")
print(f"version     : {mk.get('version', '(unset)')}")
print(f"plugins     : {len(plugins)}")
print(f"layout      : {'shared root (old)' if shared_root else 'self-contained plugin dirs'}")
print()

if shared_root:
    print("VERDICT: pre-3.0.0 build. Skills are declared by path in marketplace.json,")
    print("         which is where every previous problem came from. Replace it.\n")
elif len(plugins) == 15:
    print("VERDICT: 3.0.0 layout. Current.\n")

bad = 0
total = 0
for p in plugins:
    src = os.path.join(root, p.get("source", ""))
    skills = glob.glob(os.path.join(src, "skills", "*", "SKILL.md"))
    agents = glob.glob(os.path.join(src, "agents", "*.md"))
    pj = os.path.join(src, ".claude-plugin", "plugin.json")
    manifest = os.path.isfile(pj)
    declared = 0
    if manifest:
        try:
            declared = len(json.load(open(pj, encoding="utf-8")).get("skills") or [])
        except Exception:
            declared = -1
    total += len(skills)
    problems = []
    if not os.path.isdir(src):
        problems.append("source missing")
    if not manifest:
        problems.append("no plugin.json")
    if not skills:
        problems.append("no skills on disk")
    if manifest and declared != len(skills):
        problems.append(f"plugin.json declares {declared}, disk has {len(skills)}")
    flag = ("   <-- " + ", ".join(problems)) if problems else ""
    if problems:
        bad += 1
    entry_skills = len(p.get("skills") or [])
    if entry_skills != len(skills):
        problems.append(f"entry declares {entry_skills}")
        flag = "   <-- " + ", ".join(problems)
    print(f"  {p['name']:<30} v{p.get('version','?'):<7} disk={len(skills):<3} "
          f"plugin.json={declared:<3} entry={entry_skills:<3} agents={len(agents)}{flag}")

print(f"\ntotal skills discovered: {total}")
print("Expected for 3.2.0: 15 plugins, 67 skills.\n")
print("OK" if not bad and total == 67 else "Not deployable as-is.")
