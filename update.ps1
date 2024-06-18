
# PowerShell script to look for updates on the GitHub repository, update the application, and run the program.

# Variables
$repoDir = "C:\CiscoSwitchPortApp"
$repoUrl = "https://github.com/gp3264/CiscoSwitchPortApp.git"

# Navigate to the repository directory
if (-not (Test-Path $repoDir)) {
    Write-Error "Repository directory not found."
    exit 1
}
cd $repoDir

# Pull the latest updates from GitHub
#git pull

# Set up the Python virtual environment and install updated dependencies
& .\venv\Scripts\Activate.ps1
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\pip.exe install -r requirements.txt

# Set up the Python virtual environment
& .\venv\Scripts\Activate.ps1


# Run the Flask application
$env:FLASK_APP = "run:app_instance"
$env:FLASK_ENV = "development"
#.\venv\Scripts\flask.exe run
#.\venv\Scripts\python.exe run.py
sleep 8