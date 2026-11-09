@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto dependencies
where py >nul 2>&1
if errorlevel 1 goto use_python
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto python_missing
py -3 -m venv .venv
if errorlevel 1 goto failed
goto dependencies
:use_python
python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto python_missing
python -m venv .venv
if errorlevel 1 goto failed
:dependencies
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
".venv\Scripts\python.exe" Main.py
if errorlevel 1 goto failed
exit /b 0
:python_missing
echo Python 3.10 ou plus recent est necessaire. Installer Python puis relancer.
pause
exit /b 1
:failed
echo Echec. Lire le message ci-dessus. Verifier Python et la connexion Internet.
pause
exit /b 1
