#!/usr/bin/env python3
"""Deploy this build into a marketplace repo. Same job as deploy.ps1, no PowerShell needed.

    python deploy.py D:\\AIAutomation\\my-agent-marketplace
    python deploy.py D:\\AIAutomation\\my-agent-marketplace --push

Clears the target except .git, copies everything including hidden directories,
then fails loudly if the manifest did not land or disagrees with what is on disk.
"""
import json, os, shutil, subprocess, sys, glob

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    push = '--push' in sys.argv
    if not args:
        sys.exit(__doc__)
    repo = os.path.abspath(args[0])
    src = os.path.dirname(os.path.abspath(__file__))

    src_manifest = os.path.join(src, '.claude-plugin', 'marketplace.json')
    if not os.path.isfile(src_manifest):
        sys.exit(f"No .claude-plugin/marketplace.json in {src}.\n"
                 "Extract the zip fully and run this from inside the extracted folder.")
    if not os.path.isdir(repo):
        sys.exit(f"Target repo not found: {repo}")

    # Overlapping paths would delete the source while clearing the target.
    src_r, repo_r = os.path.realpath(src), os.path.realpath(repo)
    if src_r == repo_r:
        sys.exit(f"Source and target are the same folder:\n  {src_r}\n\n"
                 "The build is already in the repo, so there is nothing to deploy.\n"
                 "Verify and push instead:\n"
                 "  python scripts/check-deployment.py\n"
                 '  git add -A && git commit -m "Update marketplace" && git push')
    if repo_r.startswith(src_r + os.sep) or src_r.startswith(repo_r + os.sep):
        sys.exit(f"Source and target are nested ({src_r} / {repo_r}).\n"
                 "Extract the build somewhere separate and run it from there.")

    src_version = json.load(open(src_manifest, encoding='utf-8'))['version']
    print(f"Source : {src}\nTarget : {repo}\nBuild  : {src_version}\n")

    print("Clearing target (keeping .git)...")
    for entry in os.listdir(repo):
        if entry == '.git':
            continue
        p = os.path.join(repo, entry)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    print("Copying build (hidden directories included)...")
    for entry in os.listdir(src):
        if entry == '.git':
            continue
        s, d = os.path.join(src, entry), os.path.join(repo, entry)
        shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)

    manifest = os.path.join(repo, '.claude-plugin', 'marketplace.json')
    if not os.path.isfile(manifest):
        sys.exit("FAILED: .claude-plugin/marketplace.json missing from the target.")

    mk = json.load(open(manifest, encoding='utf-8'))
    on_disk = len(glob.glob(os.path.join(repo, 'plugins', '*', 'skills', '*', 'SKILL.md')))
    missing = [p['name'] for p in mk['plugins']
               if not os.path.isfile(os.path.join(repo, p['source'], '.claude-plugin', 'plugin.json'))]

    print(f"\nDeployed:\n  version : {mk['version']}\n  plugins : {len(mk['plugins'])}"
          f"\n  skills  : {on_disk} discovered")
    if missing:
        sys.exit("Plugins missing plugin.json: " + ", ".join(missing))
    if on_disk != 67:
        sys.exit(f"Expected 67 skills, found {on_disk}.")
    if mk['version'] != src_version:
        sys.exit("Version mismatch after copy — the manifest was not replaced.")
    print("  status  : OK")

    if push:
        subprocess.run(['git', 'add', '-A'], cwd=repo, check=True)
        subprocess.run(['git', 'commit', '-m', f"Deploy qz-agent-clusters {mk['version']}"],
                       cwd=repo, check=True)
        subprocess.run(['git', 'push'], cwd=repo, check=True)
        print("\nPushed. Now run in Claude Code:")
    else:
        print("\nNot pushed (add --push). Then run in Claude Code:")
    print(f"  /plugin marketplace update {mk['name']}")
    print("  /reload-plugins")


if __name__ == '__main__':
    main()
