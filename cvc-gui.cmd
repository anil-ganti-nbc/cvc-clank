@echo off
set "PYTHONW=%LOCALAPPDATA%\Python\bin\pythonw.exe"
if not exist "%PYTHONW%" set "PYTHONW=pythonw.exe"
start "CVC Clank" "%PYTHONW%" "%~dp0run_gui.py" --root "%~dp0"
