from setuptools import setup, find_packages  # Python packaging tools
import os          # Operating system functionality (check file/folder existence)
import subprocess  # Run external commands (create virtual environment, run pip)
import sys         # System information (current Python path, OS type)

# Create virtual environment in root folder
venv_path = 'venv'

# Check if venv folder already exists
if not os.path.exists(venv_path):
    # Create virtual environment using subprocess
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
    print(f"Virtual environment created at {venv_path}")

    # Get pip path based on OS (different OS have different virtual environment structures)
    if sys.platform == 'win32':
        # Windows
        pip_path = os.path.join(venv_path, 'Scripts', 'pip')
    else:
        # macOS/Linux
        pip_path = os.path.join(venv_path, 'bin', 'pip')

    # Use pip from virtual environment to install dependencies
    print("Installing requirements...")
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
    print("Requirements installed successfully!")
else:
    # If venv folder already exists, skip creation to avoid duplication
    print(f"Virtual environment already exists at {venv_path}")
