# Contributing

This repository is a public architecture documentation starter. Contributions
should improve the generic workflow, template quality, and public-safe default
configuration.

## Contribution Rules

- Keep templates generic and reusable.
- Do not add organization-specific, customer-specific, or regulated internal
  information.
- Prefer changes that help multiple documentation teams adopt the starter with
  minimal rewiring.
- Keep generated artifacts out of the repo unless the change is specifically
  about sample output handling.

## Branching

Recommended branch model:

```text
main        stable default branch
develop     integration branch for upcoming changes
feature/*   short-lived feature branches
fix/*       short-lived fix branches
```

If your hosting platform supports template repositories, mark this repo as a
template after the initial baseline is stable.

## Before Opening a Pull Request

Run the local checks:

```bash
python scripts/lint-frontmatter.py --path .
python scripts/lint-mermaid.py --path .
python scripts/lint-prose.py --no-exit
markdownlint .
```

## Pull Requests

1. Describe what changed and why.
2. Call out any starter-template taxonomy changes explicitly.
3. Note whether the change should also be mirrored into downstream content
   repositories.

## Code of Conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).

