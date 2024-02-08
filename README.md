# F1 Prediction Project 🏎️

This project aims to predict Formula 1 race outcomes using machine learning.


## Introduction

Dive into this project and showcase your skills in DevOps and MLOps by creating an AI/ML application inspired by your hobbies or interests. This isn't just an assignment; it's a key part of your professional portfolio, demonstrating your grasp of advanced concepts like continuous training and MLOps to future employers. Embrace this opportunity, let your creativity shine, and show us what you're capable of in this exciting field. We're eager to see your innovations – give it your best and enjoy the journey!

We worked on a full automated project for ***Formula One race winner predictions***.

## Getting Started

### Prerequisites

Ensure you have Git, Python & Make installed on your system.

### Installation

1. **Clone the GitHub Repository**
    Clone the project to your local machine using the following command
    ```bash
    git clone https://github.com/TBillaudeau/F1-ML-Prediction
    ```

2. **Access the Project Directory**
    Change into the project directory
    ```bash
    cd F1-ML-Prediction
    ```

3. **Set Up the Environment**
    Create a virtual environment and install the required dependencies
    ```bash
    make setup
    ```

4. **Update Packages (Optional)**
    To update all packages in your environment to their latest versions
    ```bash
    make update
    ```

### Usage

1. **Import Data**
    Run the script to import necessary data for the project
    ```bash
    make import_data
    ```

2. **Run Unit Tests**
    To ensure the basic units of code work as expected
    ```bash
    make unit_tests
    ```

3. **Run Integration Tests**
    To test combined parts of the application to ensure they work together correctly
    ```bash
    make integration_tests
    ```

4. **Run All Tests**
    Execute all available tests, including both unit and integration tests
    ```bash
    make tests
    ```

5. **Train and Save the Model**
    To train the machine learning model and save it
    ```bash
    make train_and_save_model
    ```

6. **Build Docker Image**
    To build the Docker image
    ```bash
    make build_docker
    ```

7. **Run Streamlit App**
    To run the Streamlit app
    ```bash
    make run_streamlit
    ```

8. **Clean Up**
    Remove the virtual environment and clean the project directory
    ```bash
    make clean
    ```

## Automatic workflows
> Get new data every Tuesday at 03am

> Automatic test on push to master branch

> Train model, save model & deploy to Northflank

### Actions secrets
```
DOCKERHUB_USERNAME
DOCKERHUB_ACCESSTOKEN

GH_TOKEN
 
NORTHFLANK_API_KEY
PROJECT_ID
SERVICE_ID
```

---
> A project made with a lot of ❤️ by **ARBEY** Louis, **BILLAUDEAU** Thomas and **CRETINON** Pierre-Louis