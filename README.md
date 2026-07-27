# code-crafters-lib-mgmt-sys
A repository for BookVault, a library management system developed by 'Code Crafters', a group of Ivy Tech students enrolled in the SDEV 265 course.

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

## Building a Windows demo release (one-directory)

To make a zero-setup downloadable release (Windows), the easiest approach is
to build a PyInstaller "onedir" bundle and upload the resulting `dist/BookVault.zip`
to GitHub Releases. The app will create `data/library.db` automatically on first run
if it is missing; this build includes the `data/` folder so the DB is persistent
next to the executable.

From the project root (Windows PowerShell):

```powershell
# one-time: build and zip release (creates .venv, installs pyinstaller)
.\scripts\build-windows.ps1

# After that, unpack dist\BookVault.zip and run BookVault\BookVault.exe
```

Notes:
	to a persistent path on first run (e.g. `%APPDATA%/BookeVault/library.db`).

## Downloading & running the Windows release

After a release is published on GitHub you can download and run the demo like this:

1. Download the `BookVault.zip` asset from the release on the repository Releases page.
2. Extract all files to your desired "install" location (a regular folder on your PC).
3. Open the extracted folder and run `BookVault.exe` (double-click or run from PowerShell).
Notes for users:
	next to the executable. The app will also create `data/library.db` if it is missing.
- Windows SmartScreen may warn for unsigned binaries — choose "More info → Run anyway"
	to proceed with the demo.

All commands should complete without errors.