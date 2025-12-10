# finance_mcp Constitution
<!-- 
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles: N/A (initial creation)
- Added sections: Core Principles, Development Workflow, API & Package Development, Governance
- Removed sections: N/A
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

## Core Principles

### I. Code Structure & Modularity
- Files must not exceed 500 lines; refactor into smaller modules or helpers proactively.
- Code must be organized by feature or responsibility to ensure a clean and understandable structure.
- Standardize imports and prefer relative imports within packages.

### II. Data Handling & Validation
- Use `TypedDict` for all dictionaries with known key/value types to enforce data structures.
- Define shared, reusable keys or values in a `constants.py` file to avoid magic strings and promote consistency.
- Employ `Pydantic` for robust data validation and schema enforcement at runtime.

### III. Code Quality & Style (NON-NEGOTIABLE)
- All code must strictly adhere to PEP8 compliance.
- Type hints are mandatory for all functions, variables, and class members.
- All Python code must be formatted with `black` before committing.
- Single-character variable names and the use of Python keywords as variable names are forbidden.

### IV. Testing & Reliability
- All tests must be placed in the `/tests` directory, mirroring the main project structure.
- `pytest` is the mandatory framework for all tests.
- Every feature or change requires tests covering the expected use case, at least one edge case, and at least one failure case.
- For bug fixes, an initial test replicating the bug must be added, and `BUGS_LOG.md` must be updated.

### V. Documentation & Clarity
- All functions and classes must have Google-style docstrings.
- For any non-obvious logic, an inline comment prefixed with `# Reason: ` is required to explain the rationale.
- `README.md` must be updated whenever features, dependencies, or setup steps change.

## Development Workflow

- At the start of any session, check for a `specs/` directory and corresponding `plan.md`, `spec.md`, and `tasks.md` files. These are the primary sources of truth for project planning and tasks.
- The `.venv` virtual environment must be used for all Python commands, and dependencies from `pyproject.toml` must be installed.
- Always check `UPDATES.md` for the latest changes and `BUGS_LOG.md` for known issues before starting work.

## API & Package Development

- This section applies only when developing APIs or packages.
- A pre-flight check is mandatory before implementing API methods, including verifying against official documentation.
- FastAPI must be used for building APIs, SQLModel for the ORM, and `pydantic_ai` for LLM agent creation.
- Use LangGraph for LLM agent orchestration.

## Governance

- All development must comply with the principles outlined in this constitution.
- Ambiguous requests must be clarified before implementation; do not assume context.
- Hallucinating libraries, functions, or file paths is forbidden. Always verify the existence and documentation of packages and modules.
- Code may not be deleted or overwritten unless explicitly instructed or as part of a documented task.
- A step-by-step plan must be created and confirmed before proceeding with any implementation.

**Version**: 1.0.0 | **Ratified**: 2025-12-01 | **Last Amended**: 2025-12-01