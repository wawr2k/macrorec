@echo off
REM Batch file wrapper for package_choaga_mods.py
REM This script can be run from anywhere - it will find the ok-dna working directory

cd /d "%~dp0"

REM Try py launcher first (Windows), then python
py package_choaga_mods.py 2>nul
if %ERRORLEVEL% NEQ 0 (
    python package_choaga_mods.py
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Package created successfully!
) else (
    echo.
    echo Failed to create package. Check error messages above.
)

pause

