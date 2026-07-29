#!/usr/bin/env python3
"""Tell me what is actually deployed, and which build it is.

    python3 scripts/check-deployment.py                 # this directory
    python3 scripts/check-deployment.py /path/to/repo    # somewhere else

Build history:
    0.1.0   4 cluster plugins, 1 (broken) skill each
    1.0.0   15 plugins, 1 skill each
    2.0.0   15 plugins, 67 task-level skills
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
claimed = sum(len(p.get("skills", [])) for p in plugins)
on_disk = len(glob.glob(os.path.join(root, "skills", "**", "SKILL.md"), recursive=True))

print(f"marketplace : {mk.get('name')}")
print(f"version     : {mk.get('version', '(unset)')}")
print(f"plugins     : {len(plugins)}")
print(f"skills      : {claimed} claimed by the manifest / {on_disk} SKILL.md files on disk")
print()

verdict = None
if len(plugins) == 4:
    verdict = "0.1.0 layout — four cluster plugins. Two builds behind."
elif len(plugins) == 15 and claimed == 15:
    verdict = "1.0.0 layout — 15 plugins with one skill each. One build behind."
elif len(plugins) == 15 and claimed > 15:
    verdict = "2.0.0 layout — 15 plugins with task-level skills. Current."
if verdict:
    print(f"VERDICT: {verdict}\n")

# The mixed state: new skill tree copied in, old manifest left behind.
mixed = []
for p in plugins:
    for s in p.get("skills", []):
        d = os.path.join(root, s)
        if os.path.isdir(d) and not os.path.isfile(os.path.join(d, "SKILL.md")):
            nested = glob.glob(os.path.join(d, "*", "SKILL.md"))
            if nested:
                mixed.append((p["name"], s, len(nested)))

if mixed:
    print("*** MIXED STATE — skills/ was updated but marketplace.json was not ***")
    print("The manifest points at directories that now contain nested skills.")
    print("Replace .claude-plugin/marketplace.json with the one from this build.\n")
    for name, s, n in mixed[:5]:
        print(f"  {name}: '{s}' has no SKILL.md but contains {n} skill dirs")
    print()

bad = 0
for p in plugins:
    oks = [os.path.isfile(os.path.join(root, s, "SKILL.md")) for s in p.get("skills", [])]
    flag = "" if (oks and all(oks) and len(p.get("agents", [])) == 1) else "   <-- check"
    if flag:
        bad += 1
    print(f"  {p['name']:<30} v{p.get('version','?'):<7} "
          f"skills={len(p.get('skills', []))} agents={len(p.get('agents', []))}{flag}")

print()
if claimed != on_disk:
    print(f"MISMATCH: {on_disk - claimed:+d} skills on disk are not claimed by any entry.")
print("OK" if not bad and claimed == on_disk else "Not deployable as-is.")
