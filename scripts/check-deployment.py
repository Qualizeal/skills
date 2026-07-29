#!/usr/bin/env python3
"""Tell me what is actually deployed.

Run this against the repo you pushed, before blaming the client:

    python3 scripts/check-deployment.py                    # this directory
    python3 scripts/check-deployment.py /path/to/repo      # somewhere else
"""
import json, sys, os, glob

root = sys.argv[1] if len(sys.argv) > 1 else "."
path = os.path.join(root, ".claude-plugin", "marketplace.json")

if not os.path.isfile(path):
    sys.exit(f"No marketplace.json at {path} — this is not a marketplace root.")

mk = json.load(open(path, encoding="utf-8"))
plugins = mk.get("plugins", [])

print(f"marketplace : {mk.get('name')}")
print(f"version     : {mk.get('version', '(unset)')}")
print(f"entries     : {len(plugins)}")
print()

if len(plugins) == 4 and all(len(p.get("skills", [])) == 1 for p in plugins):
    parents = [p["skills"][0] for p in plugins if p.get("skills")]
    if any(not os.path.isfile(os.path.join(root, s, "SKILL.md")) for s in parents):
        print("*** THIS IS THE OLD 0.1.0 LAYOUT ***")
        print("Four cluster plugins, each pointing at a parent folder rather than a")
        print("skill directory. Every cluster will show exactly one skill, named after")
        print("the folder. Replace this repo with the current build.\n")

for p in plugins:
    skills = p.get("skills", [])
    agents = p.get("agents", [])
    ok = []
    for s in skills:
        ok.append("OK" if os.path.isfile(os.path.join(root, s, "SKILL.md")) else "NO SKILL.md")
    flag = "" if (len(skills) == 1 and len(agents) == 1 and ok == ["OK"]) else "   <-- check"
    print(f"  {p['name']:<30} v{p.get('version','?'):<8} "
          f"skills={len(skills)} agents={len(agents)} {','.join(ok)}{flag}")

print()
on_disk = len(glob.glob(os.path.join(root, "skills", "*", "*", "SKILL.md")))
claimed = sum(len(p.get("skills", [])) for p in plugins)
print(f"SKILL.md files on disk: {on_disk} | claimed by entries: {claimed}")
if on_disk != claimed:
    print("Mismatch — some skills will not load.")
