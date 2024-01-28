# Name of the virtual environment
VENV_NAME=formulaOneEnv

# Command to create virtual environment
VENV_COMMAND=python3 -m venv

# Python version
PYTHON_VERSION=3

# Python version
PYTHON=$(VENV_NAME)/bin/python$(PYTHON_VERSION)

# Default target
all: setup

# Setup Python environment
setup:
	$(VENV_COMMAND) $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt
	echo "Python environment setup ! (run '. $(VENV_NAME)/bin/activate' to enter)"

# Update all packages in the environment
update:
	. $(VENV_NAME)/bin/activate && pip install --upgrade pip && pip install --upgrade -r requirements.txt
	echo "All packages updated !"

# Run all the tests
tests:
	$(PYTHON) -m pytest
	echo "All tests passed !"

# Clean the environment
clean:
	rm -rf $(VENV_NAME)
	echo "Environment cleaned ! (run 'deactivate' to exit)"