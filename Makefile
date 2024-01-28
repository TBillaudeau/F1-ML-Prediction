# Name of the virtual environment
VENV_NAME=formulaOneEnv

# Python version
PYTHON_VERSION=3

# Python path
PYTHON=$(VENV_NAME)/bin/python$(PYTHON_VERSION)

# Detect the operating system
ifeq ($(OS),Windows_NT) 
    activate_script := $(VENV_NAME)\Scripts\activate
else
    activate_script := . $(VENV_NAME)/bin/activate
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
	$(PYTHON) -m pytest
	echo "All tests passed !"

# Clean the environment
clean:
	rm -rf $(VENV_NAME)
	echo "Environment cleaned ! (run 'deactivate' to exit)"

# Run import_data.py file
import_data:
	$(PYTHON) src/import_data.py