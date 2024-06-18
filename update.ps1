
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
git pull

# Set up the Python virtual environment and install updated dependencies
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run the Flask application
$env:FLASK_APP = "app"
flask run

sleep 15
