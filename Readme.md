# Check python version

python --version

# Create virtual environment

python -m venv .venv

# Activate virtual environment

.venv\Scripts\activate

# Deactivate virtual environment

deactivate

# Update pip if required

python -m pip install --upgrade pip

# Install package

python -m pip install matplotlib

# Uninstall package

pip3 uninstall gitpy

# List packages installed with Pip

pip freeze

# Install packages in requirements file

Create requirements.txt and past the packages
pip install -r requirements.txt
or
pip3 install -r requirements.txt
