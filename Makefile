# Name of the virtual environment
VENV_NAME=formulaOneEnv

# Python version
PYTHON_VERSION=3

# Detect the operating system
ifeq ($(OS),Windows_NT) 
	activate_script := $(VENV_NAME)\Scripts\activate
	remove_script := if exist $(VENV_NAME) rmdir /s /q $(VENV_NAME)
	python := $(VENV_NAME)\Scripts\python
else
	activate_script := . $(VENV_NAME)/bin/activate
	remove_script := if [ -d "$(VENV_NAME)" ]; then rm -rf $(VENV_NAME); fi
	python := $(VENV_NAME)/bin/python$(PYTHON_VERSION)
endif

# ------------------------------------------------------ #

# Default target
all: setup

# Setup Python environment
setup:
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	$(activate_script) && pip install -r requirements.txt
	echo "Python environment setup ! (run '$(activate_script)' to enter)"

# Update all packages in the environment
update:
	$(activate_script) && pip install --upgrade pip && pip install --upgrade -r requirements.txt
	echo "All packages updated !"

# Run all the tests
tests:
	$(python) -m pytest
	echo "All tests passed !"

# Clean the environment
clean:
	$(remove_script)
	echo "Environment cleaned ! (run 'deactivate' to exit)"

# Run import_data.py file
import_data:
	$(python) src/import_data.py