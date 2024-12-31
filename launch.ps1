# Change to the script's directory
cd $PSScriptRoot

# Create the log directory if it doesn't exist
$logDirectory = "log\logs"
if (-not (Test-Path $logDirectory)) {
    New-Item -ItemType Directory -Force -Path $logDirectory
}

# Define the log file paths
$mainLogFile = Join-Path $logDirectory "main.log"
$winLogFile = Join-Path $logDirectory "win.log"

# Start main.py and capture its process ID, redirecting output to main.log
$mainProcess = Start-Process -FilePath "pythonw" -ArgumentList "main.py" -PassThru -RedirectStandardOutput $mainLogFile

# Start win.py without a console window, redirecting output to win.log and wait for it to exit
Start-Process -FilePath "pythonw" -ArgumentList "win.py" -RedirectStandardOutput $winLogFile -Wait

# Kill the main.py process
Stop-Process -Id $mainProcess.Id -Force
