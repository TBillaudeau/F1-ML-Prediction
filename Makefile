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

# Clean the environment
clean:
	$(remove_script)
	echo "Environment cleaned ! (run 'deactivate' to exit)"

# Run import_data.py file
import_data:
	$(python) src/import_data.py

# Run train_and_save_model.py file
train_and_save_model:
	$(python) src/train_and_save_model.py

# Run unit tests
unit_tests:
	$(python) -m unittest test/test_import_data.py
	echo "Unit tests passed !"

# Run integration tests
integration_tests:
	$(python) -m unittest test/integration_test.py
	echo "Integration test passed !"

# Run app tests
test_app:
	$(python) test/test_app.py
	echo "App tests passed !"

# Run end to end tests
endtoend_test_app:
	$(python) -m unittest test/endtoend_test.py
	echo "End to end tests passed !"


# Run all tests
tests:
	$(python) -m pytest
	echo "All tests passed !"

# Build Docker image
build_docker:
	docker build -t f1-ml-prediction .

# Run Streamlit app
run_streamlit:
	$(python) -m streamlit run streamlit/app.py