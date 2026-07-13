# Architecture Documentation Starter Repository

This repository is a public starting point for architecture documentation teams.
Markdown and structured YAML metadata are the source format.
Generated documents such as DOCX and PDF are build artifacts, not hand-edited deliverables.

The rendering and validation tooling lives in the separate public repo
[`dac-toolkit`](https://github.com/KhalilGibrotha/dac-toolkit).

## Repository Structure

```text
.
|-- docs/           Published or near-final architecture content
|-- initiatives/    Active initiative-specific architecture work
|-- patterns/       Reusable architectural and operational patterns
|-- templates/      Document skeletons and front matter stubs
|-- governance/     Review packets, checklists, ownership maps
|-- decisions/      Architecture decision records (ADRs)
|-- diagrams/       Source diagrams and shared image assets
|-- notes/          Raw working capture that may later become formal docs
|-- references/     Supporting knowledge such as acronyms and technology sheets
|-- manifests/      Render manifests for batch document workflows
|-- assets/         Shared logos and brand-safe repository assets
|-- vars/           Organization identity and structured data
|-- build/          Local build output such as rewritten markdown and generated diagrams
|-- exports/        Optional published DOCX/PDF release artifacts
`-- archive/        Retired or superseded content
```

## Document Generation Workflow

This is a content repository. The document builder lives in `dac-toolkit`.

### Setup

```bash
# Clone both repos side by side
git clone https://github.com/KhalilGibrotha/dac-toolkit.git
git clone <your-org>/<this-repo>.git

# Install the builder
(cd dac-toolkit/docx_builder && pip install -e .)

# Sync Vale packages once per clone
(cd <this-repo> && vale sync)
```

### Build all manifest-managed documents

Run from the parent directory that contains both repos:

```bash
bash dac-toolkit/scripts/build-docs.sh <this-repo>
```

This workflow expects:

- organization metadata in `vars/org.yaml`
- an optional shared logo at `assets/logo/logo.png`
- one or more render manifests under `manifests/`

### Build a single document

```bash
docx-build docs/example_architecture-overview.md \
  --org vars/org.yaml \
  --output exports/example_architecture-overview.docx
```

## Build Artifacts vs Published Artifacts

Use two output areas on purpose:

- `build/` is local working output. Keep rewritten markdown, generated diagram assets, lint reports, and scratch render output here.
- `exports/` is for intentional deliverables. Commit files here only when you want versioned review or release artifacts in git.

Suggested `build/` layout:

```text
build/
|-- rewritten/
|-- diagrams/
|-- reports/
`-- docx/
```

Recommended behavior:

- write routine local output to `build/`
- write final deliverables to `exports/` only when needed
- do not edit generated files directly

## Recommended Manifest Layout

The repository includes `manifests/render-manifest.yaml` as a working example.
The current wrapper-friendly pattern is:

- one root manifest for common defaults
- document entries with stable `id` values
- build output routed to `build/`
- final named exports routed to `exports/` only when intentionally desired

## Where Things Go

| Content type | Folder |
|---|---|
| Published platform or domain architecture | `docs/` |
| Active initiative work | `initiatives/<name>/` |
| Reusable patterns | `patterns/` |
| Templates and front matter stubs | `templates/` |
| Review packets and checklists | `governance/` |
| Architecture decision records | `decisions/` |
| Diagram source and shared images | `diagrams/` |
| Raw capture and working notes | `notes/` |
| Supporting references | `references/` |
| Shared organization metadata | `vars/` |
| Shared logo and public assets | `assets/` |
| Render manifests | `manifests/` |
| Local build output | `build/` |
| Optional published artifacts | `exports/` |
| Retired content | `archive/` |

## Authoring Conventions

- Use YAML front matter for formal documents.
- Keep headings unnumbered in source markdown. Let the builder apply numbering.
- Keep reusable source diagrams in `diagrams/`.
- Prefer `assets/logo/logo.png` for a repository-wide default cover logo.
- Keep repository-wide organization metadata in `vars/org.yaml`.
- Use templates from `templates/` as your starting point rather than copying old published documents.

## Quality Tooling

The starter includes a minimal baseline for:

- front matter validation: `python scripts/lint-frontmatter.py --path .`
- Mermaid fence preflight: `python scripts/lint-mermaid.py --path .`
- Vale prose lint: `python scripts/lint-prose.py --no-exit`
- markdownlint structure lint: `markdownlint .`

Recommended Visual Studio Code extensions are included in `.vscode/extensions.json`.

## Using This Repo in Dev Spaces

If you maintain a Dev Spaces workspace repo that clones content repos on startup,
add this repository to that clone list after you publish it.

Example entry:

```text
https://github.com/<your-org>/architecture-docs-starter
```

If you also clone `dac-toolkit`, keep the repos side by side so wrapper scripts
can resolve shared tooling consistently.

## Publishing Guidance

Before publishing this starter for wider reuse:

1. Replace placeholder organization values in `vars/org.yaml.example`.
2. Add or adjust templates that reflect your preferred document taxonomy.
3. Decide whether `exports/` should stay mostly ignored or hold formal release artifacts.
4. Publish the repo as a template or public seed repository in your Git hosting platform.

