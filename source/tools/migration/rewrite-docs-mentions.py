#!/usr/bin/env python3
"""
    rewrite-docs-mentions

    Rewrites prose mentions of the retired distributions in AGENTS.md and README.rst so they
    name codecraftai-foundations instead. Handles Markdown single backticks and RST double
    backticks. After substitution, a list that now names foundations more than once is
    collapsed to a single mention, and dangling separators are tidied.

    Without --apply, prints a unified diff per file and changes nothing.

    Usage:
        rewrite-docs-mentions [--apply] FILE [FILE ...]
"""

import argparse
import difflib
import re
import sys

RETIRED = ("codecraftai-errors", "codecraftai-interfaces", "codecraftai-waiting")
NEW = "codecraftai-foundations"


def rewrite(text: str) -> str:
    for name in RETIRED:
        text = re.sub(r"(`+)" + re.escape(name) + r"\1", lambda m: m.group(1) + NEW + m.group(1), text)

    # Collapse "`F`, `F`" / "`F`,\n`F`" / "`F`, and `F`" / "`F` and `F`" repeated mentions.
    for _ in range(4):
        text = re.sub(r"(`+)" + NEW + r"\1,?\s+(?:and\s+)?(`+)" + NEW + r"\2", lambda m: m.group(1) + NEW + m.group(1), text)

    # "`F`, and `X`" reads badly when only two items remain in a sentence; leave Oxford commas
    # alone otherwise, they are correct for three or more items.
    text = re.sub(r"depends on (`+)" + NEW + r"\1, and ", lambda m: "depends on " + m.group(1) + NEW + m.group(1) + " and ", text)
    text = re.sub(r"builds on (`+)" + NEW + r"\1, and ", lambda m: "builds on " + m.group(1) + NEW + m.group(1) + " and ", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(prog="rewrite-docs-mentions")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    changed = 0
    for path in args.files:
        with open(path, encoding="utf-8") as handle:
            before = handle.read()
        after = rewrite(before)
        if after == before:
            continue
        changed += 1
        if args.apply:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(after)
        else:
            sys.stdout.writelines(difflib.unified_diff(before.splitlines(True), after.splitlines(True), path, path))
            sys.stdout.write("\n")
    print("{}: {} file(s) changed".format("applied" if args.apply else "dry run", changed), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
