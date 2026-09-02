# Consolidation tooling

Scripts used on 2026-09-02 to consolidate `codecraftai-errors`, `codecraftai-interfaces`,
`codecraftai-waiting` and `Freezable` (from `codecraftai-xmodules`) into this package. They are
kept for reference and for any repository created from an old checkout that still pins the
retired names.

- `rewrite-foundations-deps.py` rewrites a repository's `pyproject.toml` so the retired
  dependencies become one dependency on `codecraftai-foundations`, optionally bumping the patch
  version so the publish workflow fires.
- `rewrite-docs-mentions.py` rewrites prose mentions of the retired distributions in `AGENTS.md`
  and `README.rst`.
- `migrate-repo.sh` runs the whole per-repository procedure: fast-forward, rewrite, add the
  licensed-index credential step to the merge gate, clear poetry's cached source listing, relock,
  verify that the retired names resolve to their 1.1.0 shims, and commit.

Always clear poetry's cached listing for the `codecraftai` source before relocking:

    poetry cache clear codecraftai --all -n

A stale listing resolves the retired names to their last real versions, and two distributions
then own the same `ccai/` files.
