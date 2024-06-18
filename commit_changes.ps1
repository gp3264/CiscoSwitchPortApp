
# PowerShell script to commit changes to the cloned repository and push to the original GitHub repository.

# Variables
$repoDir = "C:\CiscoSwitchPortApp"

# Navigate to the repository directory
if (-not (Test-Path $repoDir)) {
    Write-Error "Repository directory not found."
    exit 1
}
cd $repoDir

# Add, commit, and push changes
git add .
git commit -m "Update application with latest changes"
git push


sleep 15