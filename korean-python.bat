@echo off
set "PYTHONUTF8=1"
if "%~1"=="" (
    python "%~dp0korean_python.py" --repl
) else (
python "%~dp0korean_python.py" %*
)
exit /b %errorlevel%
