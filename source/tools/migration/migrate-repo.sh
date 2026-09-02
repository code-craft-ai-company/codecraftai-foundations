#!/usr/bin/env bash
# migrate-repo.sh REPO_DIR
#
# Phase 5 of the foundations consolidation, applied to one repository checkout:
#   1. fast-forward main from origin
#   2. rewrite pyproject dependencies onto codecraftai-foundations and bump the patch version
#   3. add the licensed-index credential step to merge_gate.yml when the workflow exists
#   4. clear poetry's cached listing for the codecraftai source and relock
#   5. verify the lock: foundations present, no retired package below its shim version
#   6. commit
# Pushing is left to the caller so each push is a separate, reviewable action.
set -euo pipefail

REPO="$1"
HERE="$(cd -- "$(dirname -- "$0")" && pwd)"
GIT_ID=(-c user.name="Myron Walker" -c user.email="myron.walker@gmail.com")
GIT_CRED=(-c credential.helper='!gh auth git-credential')

cd "$REPO"
name="$(basename "$PWD")"

git "${GIT_CRED[@]}" pull -q --ff-only origin main

if ! grep -qE '^codecraftai-(errors|interfaces|waiting) ' pyproject.toml; then
  echo "$name: nothing to rewrite"; exit 0
fi

python3 "$HERE/rewrite-foundations-deps.py" --apply --bump . >/dev/null 2>&1

GATE=.github/workflows/merge_gate.yml
if [ -f "$GATE" ] && ! grep -q "http-basic.codecraftai" "$GATE"; then
  python3 - "$GATE" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
marker = "      - name: Setup the Virtual Environment\n"
step = ('      - name: Configure the package index credential\n'
        '        run: poetry config http-basic.codecraftai deployment "${{ secrets.CCAI_ORG_READ_TOKEN }}"\n\n')
if marker in s and step not in s:
    s = s.replace(marker, step + marker, 1)
    open(p, "w").write(s)
PY
fi

poetry cache clear codecraftai --all -n >/dev/null 2>&1 || true
rm -f poetry.lock
poetry lock -q

python3 - <<'PY'
import re, sys
lock = open("poetry.lock").read()
versions = dict(re.findall(r'^name = "(codecraftai-[a-z0-9-]+)"\nversion = "([^"]+)"', lock, re.M))
assert "codecraftai-foundations" in versions, "foundations missing from lock"
for retired in ("codecraftai-errors", "codecraftai-interfaces", "codecraftai-waiting"):
    if retired in versions:
        assert versions[retired] == "1.1.0", f"{retired} resolved to {versions[retired]}, expected the 1.1.0 shim"
print("lock ok: foundations", versions["codecraftai-foundations"],
      "| shims:", {k: v for k, v in versions.items() if k in ("codecraftai-errors", "codecraftai-interfaces", "codecraftai-waiting")} or "none")
PY

git add -A
git "${GIT_ID[@]}" commit -q -F - <<EOF
Depend on codecraftai-foundations instead of the retired packages

codecraftai-errors, codecraftai-interfaces and codecraftai-waiting were
consolidated into codecraftai-foundations; import paths are unchanged.
Relocked with poetry's codecraftai source cache cleared so the retired
names resolve to their 1.1.0 shims. The merge gate now configures the
licensed-index credential from CCAI_ORG_READ_TOKEN so it can install
internal dependencies. Patch version bumped so publishing fires.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01RNvE8qyBf7V2kvVwrPv72x
EOF
echo "$name: committed $(git rev-parse --short HEAD) version $(grep '^version' pyproject.toml | cut -d'"' -f2)"
