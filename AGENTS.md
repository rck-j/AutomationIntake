# Repository Guidelines

## Project Structure & Module Organization
Keep runtime code inside `app/`, separating Flask blueprints, service helpers, and integrations into distinct subpackages. Store user-facing templates under `templates/` and any Mermaid or static assets under `static/`. Tests live in `tests/` mirroring the package layout (`tests/services/test_analyzer.py` reflects `app/services/analyzer.py`). Workflow documentation, such as intake playbooks or prompt templates, belongs in `docs/`, while repeatable tooling scripts (data seeding, diagram generation) go into `scripts/`. Track environment variables in `.env.example` and never commit real credentials.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — create and activate a local virtual environment.
- `pip install -r requirements.txt` — install the Flask backend, OpenAI client, and linting dependencies.
- `flask --app app.main run --debug` — start the intake UI with auto-reload and helpful tracebacks.
- `pytest -q` — run the full automated test suite quietly.
- `python -m scripts.generate_diagram docs/sample_process.md` — exercise the Mermaid export pipeline end to end.

## Coding Style & Naming Conventions
Format Python code with Black (88 columns) and import-sort with isort; run both before committing. Prefer type hints everywhere and treat `mypy` warnings as blockers. Use snake_case for variables and functions, PascalCase for classes, and kebab-case for CLI scripts. Keep view functions thin; push automation analysis into service modules with clear docstrings describing the AI prompts used.

## Testing Guidelines
Pytest is the single test entry point. Name files `test_<module>.py` and organize scenarios by feature, not by function names alone. Use `pytest --cov=app --cov-report=term-missing` to verify the minimum 85 % coverage. Mock external APIs (OpenAI, diagram renderers) via fixtures in `tests/conftest.py` so tests remain deterministic. Add regression tests when updating prompt templates or workflow validators to capture historical automation rules.

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat:`, `fix:`, `chore:`) with present-tense summaries under 72 characters. Each commit should be reviewable and pass lint + tests locally. PRs must include: a concise description of intent, linked issue IDs (e.g., `Closes #12`), test evidence (`pytest` output or screenshot of the intake UI), and callouts for new environment variables or migrations. Tag maintainers for code owners of touched modules and wait for at least one approval before merging.

## Security & Configuration Tips
Keep `.env` limited to mock keys locally; production secrets belong in the deployment platform’s secret store. Rotate OpenAI keys regularly and guard prompt files containing sensitive context. Run `pip-audit` monthly to catch vulnerable dependencies, and review Flask configuration so debug mode is never enabled outside local development.
