# Architecture Documentation Starter Repository

This repository is a public starting point for architecture documentation teams.
Markdown and structured YAML metadata are the source format.
Generated documents such as DOCX and PDF are build artifacts, not hand-edited deliverables.

The rendering and validation tooling lives in the separate public repo
[`dac-toolkit`](https://github.com/KhalilGibrotha/dac-toolkit).

This starter is intended to stay public-safe:

- no organization-sensitive defaults
- no internal-only taxonomy or naming
- no customer or environment-specific examples

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

This is a content repository. The document builder and manifest wrapper live in
`dac-toolkit`.

### First-Time Setup

Clone both repositories side by side:

```bash
git clone https://github.com/KhalilGibrotha/dac-toolkit.git
git clone https://github.com/<your-org>/<your-content-repo>.git
```

Your local layout should look like this:

```text
.
|-- dac-toolkit/
`-- <your-content-repo>/
```

From the content repo root, update these files before your first render:

- `vars/org.yaml`
- `assets/logo/logo.png` if you want a cover-page logo
- `manifests/render-manifest.yaml`

Then sync prose-lint packages once per clone:

```bash
cd <your-content-repo>
vale sync
```

You do not need a global `docx-build` install for the manifest workflow.
The wrapper in `dac-toolkit` creates a local virtual environment and installs
the builder there when needed.

### First Working Commands

Run these from the content repo root:

```bash
make docx-list
make docx-validate
make docx-render-all
```

This workflow expects:

- organization metadata in `vars/org.yaml`
- an optional shared logo at `assets/logo/logo.png`
- one or more render manifests under `manifests/`

This uses the toolkit-owned manifest wrapper through the starter `Makefile`.
It keeps the command surface inside the content repo while still resolving the
tooling from the sibling `dac-toolkit` clone.

### Build a Single Manifest Document

```bash
make docx-render-one DOC_ID=architecture-overview
```

### Direct Builder Example

If you want to bypass the manifest and test one source file directly:

```bash
docx-build docs/example_architecture-overview.md \
  --org vars/org.yaml \
  --logo assets/logo/logo.png \
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

This split makes it easier for teams to:

- keep routine rendering noise out of review
- publish selected artifacts intentionally
- preserve rewritten markdown and generated diagrams for troubleshooting

## Recommended Manifest Layout

The repository includes `manifests/render-manifest.yaml` as a working example.
The current wrapper-friendly pattern is:

- one root manifest for common defaults
- document entries with stable `id` values
- build output routed to `build/`
- final named exports routed to `exports/` only when intentionally desired

Example selective render pattern:

```bash
make docx-list
make docx-validate
make docx-render-one DOC_ID=architecture-overview
make docx-render-all
```

## What the Make Targets Do

- `make docx-list` shows manifest document IDs, source files, and outputs
- `make docx-validate` runs manifest and render preflight checks without writing final DOCX artifacts
- `make docx-render-one DOC_ID=<id>` renders one manifest entry
- `make docx-render-all` renders every manifest entry
- `make vale-bootstrap` syncs Vale packages for prose linting

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

## Day-to-Day Author Workflow

### 1. Start from the latest base branch

Teams usually branch from `main` or `develop`. Use whichever branch your team
has chosen as the content integration branch.

Example using `main`:

```bash
git checkout main
git pull
```

If your team uses `develop` instead:

```bash
git checkout develop
git pull
```

### 2. Create a Jira-key feature branch

Use a branch name that starts with the Jira key and a short description:

```bash
git checkout -b feature/ARCH-1234-reference-zone-model
```

### 3. Create or update document content

Typical author steps:

1. Copy a template from `templates/`.
2. Rename the file for the document you are writing.
3. Update front matter.
4. Add or update the manifest entry in `manifests/render-manifest.yaml`.
5. Add or update diagrams, assets, and linked references as needed.

### 4. Run local checks before commit

```bash
python3 scripts/lint-frontmatter.py --path .
python3 scripts/lint-mermaid.py --path .
python3 scripts/lint-prose.py --no-exit
make docx-validate
make docx-render-one DOC_ID=architecture-overview
```

Replace `architecture-overview` with the manifest ID for the document you are
actively editing.

### 5. Commit with the Jira key

```bash
git add .
git commit -m "ARCH-1234 Add reference zone model draft"
```

### 6. Push and open your pull request

```bash
git push -u origin feature/ARCH-1234-reference-zone-model
```

After that:

1. Open a pull request into your team base branch.
2. Reference the Jira ticket in the PR.
3. Include rendered output only if your team intentionally versions deliverables.

### 7. Clean up after merge

```bash
git checkout main
git pull
git branch -d feature/ARCH-1234-reference-zone-model
```

If your PR merged into `develop`, switch back to `develop` instead of `main`.

## Quality Tooling

The starter includes a minimal baseline for:

- front matter validation: `python3 scripts/lint-frontmatter.py --path .`
- Mermaid fence preflight: `python3 scripts/lint-mermaid.py --path .`
- Vale prose lint: `python3 scripts/lint-prose.py --no-exit`
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

For a Dev Spaces wrapper repo that clones content repositories on bootstrap,
add this starter to the clone list and keep `dac-toolkit` adjacent:

```text
https://github.com/<your-org>/architecture-docs-starter architecture-docs-starter
https://github.com/KhalilGibrotha/dac-toolkit dac-toolkit
```

That gives authors:

- starter templates in one repo
- shared rendering tooling in another repo
- a predictable `build/` and `exports/` model across projects

See [docs/devspaces-bootstrap-example.md](docs/devspaces-bootstrap-example.md) for a fuller example and
[templates/repos-to-clone.example.txt](templates/repos-to-clone.example.txt) for a ready-to-copy
bootstrap list.

## Publishing Guidance

Before publishing this starter for wider reuse:

1. Replace placeholder organization values in `vars/org.yaml.example`.
2. Decide whether `vars/org.yaml` should stay as a checked-in example or be
   replaced during repository creation.
3. Add or adjust templates that reflect your preferred document taxonomy.
4. Decide whether `exports/` should stay mostly ignored or hold formal release artifacts.
5. Publish the repo as a template or public seed repository in your Git hosting platform.
6. If you maintain a Dev Spaces bootstrap repo, add this repository to its clone list.

## Included Baseline Files

The starter currently includes:

- `Makefile`
- `.markdownlint.json`
- `.vale.ini`
- `.vscode/extensions.json`
- `.vscode/settings.json`
- `.github/workflows/lint.yml`
- `scripts/lint-frontmatter.py`
- `scripts/lint-mermaid.py`
- `scripts/lint-prose.py`

These are intended to be updated alongside the broader `architecture-docs`
workflow as the shared authoring standards evolve.
