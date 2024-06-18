
import os
import subprocess

# Constants
REPO_URL = "https://github.com/gp3264/CiscoSwitchPortApp.git"
REPO_DIR = "CiscoSwitchPortApp"

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
    return result.stdout

def clone_or_update_repo(repo_url, repo_dir):
    """Clone the repository if it doesn't exist, otherwise update it."""
    if not os.path.exists(repo_dir):
        print(f"Cloning repository {repo_url} into {repo_dir}...")
        run_command(f"git clone {repo_url} {repo_dir}")
    else:
        print(f"Repository {repo_dir} already exists. Pulling the latest changes...")
        os.chdir(repo_dir)
        run_command("git pull")
        os.chdir("..")

def main():
    clone_or_update_repo(REPO_URL, REPO_DIR)

if __name__ == "__main__":
    main()
