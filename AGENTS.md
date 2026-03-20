## Project Boundary

- Treat the directory from which you are invoked as the complete project root.
- Do not read parent directories, sibling directories, or nearby repositories for context.
- Do not inspect adjacent filesystems or surrounding workspace structure unless the human explicitly authorizes it.
- Assume there is nothing outside the invoked project root that is relevant by default.
- If required context is missing from the invoked project root, stop and ask instead of exploring elsewhere.

## Execution Discipline

- Obey the phase gate in `engine/data/work-instance.yaml` before mutating any downstream output directory.
- During `engine_revision`, mutate only files under `engine/`.
- Do not write to `schema-generation/` or `prose/` when the current phase forbids it.
