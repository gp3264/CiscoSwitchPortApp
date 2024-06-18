
# PowerShell script to download and install Python for Windows 10 x64, download source code from GitHub, set up the Python Flask application, and run the program.

# Variables
$pythonInstallerUrl = "hhttps://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
$pythonInstallerPath = "$env:TEMP\python-installer.exe"
$repoUrl = "https://github.com/gp3264/CiscoSwitchPortApp.git"
$installDir = "C:\CiscoSwitchPortApp"

# Check if Python is installed
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    # Download and install Python
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    # Verify Python installation
    $pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonInstalled) {
        Write-Error "Python installation failed."
        exit 1
    }
} else {
    Write-Host "Python is already installed."
}

# Check if Git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    # Download and install Git
    #$gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0-64-bit.exe"
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe"
    
    $gitInstallerPath = "$env:TEMP\git-installer.exe"
    Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath
    Start-Process -FilePath $gitInstallerPath -ArgumentList "/silent" -Wait

    # Verify Git installation
    $gitInstalled = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitInstalled) {
        Write-Error "Git installation failed."
        exit 1
    }
} else {
    Write-Host "Git is already installed."
}

# Clone the repository
if (Test-Path $installDir) {
    Remove-Item -Recurse -Force $installDir
}
git clone $repoUrl $installDir

# Set up the Python virtual environment and install dependencies
cd $installDir
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run the Flask application
$env:FLASK_APP = "app"
flask run
