# code-crafters-lib-mgmt-sys
A repository for BookVault, a library management system developed by 'Code Crafters', a group of Ivy Tech students enrolled in the SDEV 265 course.

## Downloading the app
If you want to use BookVault, download the latest release [here](https://github.com/igarcia46/code-crafters-lib-mgmt-sys/releases).

1. Download the latest `BookVault.zip` release ZIP file by clicking on it.
2. Extract the ZIP file to the desired location on your PC.
3. Open the folder and run `BookVault.exe`.

> Note: The application will be seeded with test data.

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

## Building a Windows release
From the project root:

```powershell
# one-time: build and zip release (creates .venv, installs pyinstaller)
.\scripts\build-windows.ps1
```
