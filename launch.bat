@echo off
REM Change to the directory of the script
cd /d "%~dp0"

REM Run main.py with console and save its process ID
start cmd /k "python main.py"
set /p MAIN_PID=<"%temp%\main_pid.txt"

REM Run win.py without console and wait for it to exit
pythonw win.py

REM Kill only the main.py process
TASKKILL /PID %MAIN_PID% /F

REM Pause to keep the terminal open
pause
