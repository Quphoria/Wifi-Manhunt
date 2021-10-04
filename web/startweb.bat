@echo off

@REM Change directory to script directory
cd /D "%~dp0"

@REM Run a local webserver on port 8000
python -m http.server 8000