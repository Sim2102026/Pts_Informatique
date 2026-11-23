@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 goto use_python
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto use_python
py -3 "%~dp0lancer_jeu.py" %*
goto finished

:use_python
where python >nul 2>&1
if errorlevel 1 goto missing
python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto missing
python "%~dp0lancer_jeu.py" %*
goto finished

:missing
echo Python 3.10 or newer is required. Python 3.12 is recommended.
echo Install Python from https://www.python.org/downloads/
echo Enable "Add python.exe to PATH", then launch this file again.
pause
exit /b 1

:finished
set "game_exit=%errorlevel%"
if "%game_exit%"=="0" exit /b 0
echo.
echo The game could not start or stopped with an error. Read the message above.
pause
exit /b %game_exit%
