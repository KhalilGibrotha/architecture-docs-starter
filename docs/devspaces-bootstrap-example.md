# Dev Spaces Bootstrap Example

This starter repository is meant to work cleanly alongside `dac-toolkit` in a
Dev Spaces bootstrap workflow.

## Goal

Keep content and tooling separate:

- content repo: architecture documents, templates, manifests, org metadata
- tooling repo: shared rendering, linting, and wrapper scripts

This keeps the content repo reusable while allowing platform teams to evolve
workspace automation independently.

## Recommended Workspace Shape

```text
/projects/
`-- workspace-repos/
    |-- dac-toolkit/
    `-- architecture-docs-starter/
```

## Example Clone List

If your workspace repo uses a bootstrap script like `clone-repos.sh`, a clone
list can look like this:

```text
# URL [destination relative to workspace-repos/] [optional branch]
https://github.com/KhalilGibrotha/dac-toolkit dac-toolkit develop
https://github.com/<your-org>/architecture-docs-starter architecture-docs-starter main
```

This pattern gives authors:

- shared public tooling in `workspace-repos/dac-toolkit`
- reusable starter content in `workspace-repos/architecture-docs-starter`
- a clean split between `build/` output and `exports/` deliverables

## Example Local Commands

From the parent directory that contains both repos:

```bash
cd /projects/workspace-repos/architecture-docs-starter
vale sync
python3 scripts/lint-frontmatter.py --path .
python3 scripts/lint-mermaid.py --path .
make docx-list
make docx-validate
make docx-render-one DOC_ID=architecture-overview
```

For a derived content repo, the minimal `Makefile` defaults are:

```make
PYTHON ?= python3
REPO_ROOT := $(CURDIR)
TOOLKIT_DIR ?= $(abspath $(REPO_ROOT)/../dac-toolkit)
MANIFEST ?= manifests/render-manifest.yaml
DOC_ID ?=
KROKI_URL ?= http://127.0.0.1:8000
```

## Recommended Team Practice

- keep the starter public and generic
- copy or fork it for real project work
- update `vars/org.yaml`, `assets/logo/`, and `manifests/` in the derived repo
- treat `build/` as disposable local output
- commit `exports/` only when you intend to publish or review generated artifacts
