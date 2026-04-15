# Enforcement Options

## Option A: AST Report + CI Gate (recommended)

Run the script:

- Changed files only:
  - `python scripts/ast.py --changed-only`
- Specific paths:
  - `python scripts/ast.py path/to/file.py other.py`

Outputs:

- A Markdown report to stdout (or `--out report.md`)
- Exit code `1` if violations found unless `--no-fail`

## Option B: Pylint Plugin (optional)

If you already use Pylint (or want lint-level enforcement), use the plugin in `scripts/pylint.py`.
