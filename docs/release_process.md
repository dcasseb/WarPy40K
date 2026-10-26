# Release Process

WarPy40K treats important roadmap milestones as release checkpoints.

A milestone is not considered fully closed until the following sequence is complete:

1. Implement the milestone and its regression tests.
2. Update version metadata, CHANGELOG, roadmap, and relevant documentation.
3. Run the full supported CI matrix on the exact final milestone commit.
4. Confirm formatting, import order, linting, typing, tests, coverage, and benchmark smoke checks are green.
5. Create an annotated semantic-version tag pointing to that exact validated commit.
6. Publish a GitHub Release for the tag with concise release notes covering language changes, compatibility, benchmarks, and quality status.
7. Verify that both the tag and public release resolve to the intended milestone commit.
8. Only then begin implementation of the next major roadmap milestone.

## What counts as an important milestone

By default, every completed roadmap release milestone such as `v1.5`, `v1.6`, `v1.7`, and later major runtime checkpoints requires a tag and release.

Small fixes, documentation-only changes, CI maintenance, and intermediate implementation commits do not require individual releases unless they intentionally constitute a patch release.

## Versioning

WarPy40K uses semantic-style versioning:

- milestone language/runtime releases: `v1.x.0`;
- compatible corrective releases when warranted: `v1.x.y`;
- major compatibility/runtime boundaries: future major versions such as `v2.0.0`.

Tags must never be moved after publication. If a released checkpoint needs correction, publish a new patch release instead.

## Release integrity

The release tag must point to the exact commit that passed the full release-quality CI. Release automation commits, release-note-only commits, or later development work must not silently become the tagged implementation checkpoint.

This process makes each important milestone a reproducible rollback, comparison, and historical reference point for the evolution from the Python tree-walker toward the Forge runtime.
