# code-crafters-lib-mgmt-sys
A repository for a library management system developed by 'Code Crafters', a group of Ivy Tech students enrolled in the SDEV 265 course.

## Clone the repository

git clone https://github.com/igarcia46/code-crafters-lib-mgmt-sys.git
cd code-crafters-lib-mgmt-sys

## Install development dependencies

python -m pip install -r requirements-dev.txt

These development tools are used throughout the project:

- **pytest** – Runs unit tests
- **black** – Formats Python code
- **ruff** – Checks for common coding issues and style violations

## Verify Your Setup

Run the following commands to verify your environment:

```bash
python -m compileall .
python -m black --check .
python -m ruff check .
python -m pytest -v
```

All commands should complete without errors.