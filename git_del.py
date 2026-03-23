import os
import subprocess
import sys
from datetime import datetime

PURGE_START = datetime(2026, 1, 4)
PURGE_END   = datetime(2026, 11, 28)
REPO_PATH   = "."

def run(cmd, env_extra=None):
    env = None
    if env_extra:
        env = os.environ.copy()
        env.update(env_extra)
    return subprocess.run(cmd, cwd=REPO_PATH, capture_output=True, text=True, env=env)

def get_commits():
    r = run(["git", "log", "--reverse", "--format=%H|%P|%an|%ae|%aI|%cn|%ce|%cI"])
    commits = []
    for line in r.stdout.splitlines():
        h, parents_str, an, ae, ai, cn, ce, ci = line.split("|")
        parents = parents_str.split() if parents_str.strip() else []
        commits.append((h, parents, an, ae, ai, cn, ce, ci))
    return commits

def get_tree(h):
    return run(["git", "rev-parse", f"{h}^{{tree}}"]).stdout.strip()

def get_message(h):
    return run(["git", "log", "-n", "1", "--format=%B", h]).stdout.rstrip("\n")

def make_commit(tree, parents, an, ae, ai, cn, ce, ci, msg):
    cmd = ["git", "commit-tree", tree] + [x for p in parents for x in ["-p", p]] + ["-m", msg]
    return run(cmd, env_extra={
        "GIT_AUTHOR_NAME":    an, "GIT_AUTHOR_EMAIL":    ae, "GIT_AUTHOR_DATE":    ai,
        "GIT_COMMITTER_NAME": cn, "GIT_COMMITTER_EMAIL": ce, "GIT_COMMITTER_DATE": ci,
    }).stdout.strip()

if __name__ == "__main__":
    ps = PURGE_START.strftime("%Y-%m-%d")
    pe = PURGE_END.strftime("%Y-%m-%d")

    commits = get_commits()
    to_remove = sum(1 for _, _, _, _, ai, _, _, _ in commits if ps <= ai[:10] <= pe)

    print(f"Commits in {ps} → {pe}: {to_remove}")
    if to_remove == 0:
        print("Nothing to purge.")
        sys.exit(0)

    if input("Proceed? (y/n): ").lower() != "y":
        print("Aborted.")
        sys.exit(0)

    remap = {}
    last  = None
    done  = 0

    for h, parents, an, ae, ai, cn, ce, ci in commits:
        if ps <= ai[:10] <= pe:
            remap[h] = remap.get(parents[0]) if parents else None
            continue

        new_parents = []
        for p in parents:
            resolved = remap.get(p, p)
            if resolved and resolved not in new_parents:
                new_parents.append(resolved)

        new_hash   = make_commit(get_tree(h), new_parents, an, ae, ai, cn, ce, ci, get_message(h))
        remap[h]   = new_hash
        last       = new_hash
        done      += 1
        if done % 50 == 0:
            print(f"  {done} commits rewritten...")

    if last:
        run(["git", "update-ref", "HEAD", last])

    run(["git", "reflog", "expire", "--expire=now", "--all"])
    run(["git", "gc", "--prune=now", "--aggressive"])

    print(f"\nDone. {to_remove} commits removed.")