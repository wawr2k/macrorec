@echo off
REM Batch file to add AutoFishMultiSpotTask to config.py's onetime_tasks list

cd /d "%~dp0"

REM Try py launcher first (Windows), then python
py add_autofish_to_config.py 2>nul
if %ERRORLEVEL% NEQ 0 (
    python add_autofish_to_config.py
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Done! AutoFishMultiSpotTask has been added to config.py
) else (
    echo.
    echo Failed to add entry. Please check the error message above.
)

pause

