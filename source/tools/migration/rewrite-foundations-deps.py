#!/usr/bin/env python3
"""
    rewrite-foundations-deps

    Rewrites a repository's pyproject.toml so that any dependency on the packages being
    consolidated into 'codecraftai-foundations' becomes a single dependency on foundations.

    Within each dependency section ([tool.poetry.dependencies] and every
    [tool.poetry.group.<name>.dependencies]):

      * the first line naming a retired package is replaced with the foundations line,
        unless the section already has one,
      * every other line naming a retired package is removed.

    With --bump, the patch component of [tool.poetry] version is incremented so the
    'Publish' workflow fires when the change lands on main.

    Without --apply the script prints a unified diff per repository and changes nothing.

    Usage:
        rewrite-foundations-deps [--apply] [--bump] REPO [REPO ...]

    After applying, relock each repository with a cleared source cache. Poetry caches the
    package listings of the 'codecraftai' source, and a stale listing resolves the retired
    packages to their last real versions (1.0.0) instead of the 1.1.0 shims. That installs
    two distributions owning the same ccai/ files.

        poetry cache clear codecraftai --all -n
        rm -f poetry.lock && poetry lock
"""

import argparse
import difflib
import os
import re
import sys

RETIRED = ("codecraftai-errors", "codecraftai-interfaces", "codecraftai-waiting")
FOUNDATIONS_NAME = "codecraftai-foundations"
FOUNDATIONS_LINE = 'codecraftai-foundations = { version = "<2.0.0", source = "codecraftai" }'

SECTION_RE = re.compile(r"^\[(?P<name>[^\]]+)\]\s*$")
DEP_NAME_RE = re.compile(r"^(?P<name>codecraftai-[a-z0-9-]+)\s*=")
VERSION_RE = re.compile(r'^(version\s*=\s*")(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(")\s*$')


def is_dependency_section(name: str) -> bool:
    return name == "tool.poetry.dependencies" or (
        name.startswith("tool.poetry.group.") and name.endswith(".dependencies")
    )


def rewrite(content: str, bump: bool) -> str:
    out = []
    section = None
    section_has_foundations = False

    for line in content.splitlines(keepends=True):
        header = SECTION_RE.match(line)
        if header is not None:
            section = header.group("name")
            section_has_foundations = False
            out.append(line)
            continue

        if section == "tool.poetry" and bump:
            version = VERSION_RE.match(line)
            if version is not None:
                patch = int(version.group("patch")) + 1
                line = "{}{}.{}.{}{}\n".format(
                    version.group(1), version.group("major"), version.group("minor"), patch, version.group(5)
                )
                out.append(line)
                continue

        if section is not None and is_dependency_section(section):
            dep = DEP_NAME_RE.match(line)
            if dep is not None:
                name = dep.group("name")
                if name == FOUNDATIONS_NAME:
                    section_has_foundations = True
                    out.append(line)
                    continue
                if name in RETIRED:
                    if not section_has_foundations:
                        out.append(FOUNDATIONS_LINE + "\n")
                        section_has_foundations = True
                    continue

        out.append(line)

    return "".join(out)


def process(repo: str, apply: bool, bump: bool) -> str:
    path = os.path.join(repo, "pyproject.toml")
    if not os.path.isfile(path):
        return "skip"

    with open(path, encoding="utf-8") as handle:
        before = handle.read()

    after = rewrite(before, bump)
    if after == before:
        return "unchanged"

    if apply:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(after)
    else:
        diff = difflib.unified_diff(
            before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile=path, tofile=path,
        )
        sys.stdout.writelines(diff)
        sys.stdout.write("\n")

    return "rewritten"


def main() -> int:
    parser = argparse.ArgumentParser(prog="rewrite-foundations-deps")
    parser.add_argument("--apply", action="store_true", help="write changes instead of printing diffs")
    parser.add_argument("--bump", action="store_true", help="increment the patch version so publishing fires")
    parser.add_argument("repos", nargs="+")
    args = parser.parse_args()

    counts = {"rewritten": 0, "unchanged": 0, "skip": 0}
    rewritten = []
    for repo in args.repos:
        result = process(repo, args.apply, args.bump)
        counts[result] += 1
        if result == "rewritten":
            rewritten.append(os.path.basename(os.path.normpath(repo)))

    mode = "applied" if args.apply else "dry run"
    print("{}: {} rewritten, {} unchanged, {} without pyproject".format(
        mode, counts["rewritten"], counts["unchanged"], counts["skip"]), file=sys.stderr)
    if rewritten:
        print("rewritten: " + " ".join(sorted(rewritten)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
