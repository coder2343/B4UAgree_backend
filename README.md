# B4UAgree Backend

## Overview
This repository, B4UAgree_backend, contains the backend code for the [B4UAgree](https://github.com/Amani-Alqaisi/B4UAgree) Chrome Extention repo. It includes functionalities related to privacy policy analysis.

## Contents
- `privacy_policy_score`: Evaluates the privacy policy. This file is based on the work from the [privacy-policy-evaluator](https://github.com/JPAntonisse/privacy-policy-evaluator) repository.
- `.DS_Store`: macOS system file, can be ignored.
- `.gitignore`: Git configuration file to specify untracked files.
- `README.md`: This file, providing information about the repository.
- `hello.py`: Python script containing Flask endpoints for handling privacy policy data.
- `privPolicy.txt`: Text file containing a sample privacy policy (not used in the code).
- `privacysummarizer.py`: Python script containing functions for summarizing privacy policies.
- `requirements.txt`: File specifying Python dependencies for the project.
- `test.py`: Python script for testing purposes.
- `wsgi.py`: Python script for WSGI server deployment.

## Usage locally 
1. Clone the repository:
   ```bash
   git clone https://github.com/coder2343/B4UAgree_backend.git

2. Install dependencies either with virtual env or directly on your computer:
    ```bash
   pip install -r requirements.txt

3. Run the backend server:
   ```bash
   flask --app hello run

4. Once the server is running, you can interact with it through the provided endpoints.

## Endpoints
- `/sum` (GET): Retrieves the privacy policy with the url of the privacy policy under analysis suplied in  the request's header, it summarizes and scores the policy, and returns the summary in JSON format.

## Reclaim hosting endpoint 
   'https://csc324spring2024.us.reclaim.cloud/sum' 
## Acknowledgments

We would like to acknowledge the following tools and inspirations:

- **Privacy Policy Score Calculation**: The `privacy_policy_score` file is based on the work from the [privacy-policy-evaluator](https://github.com/JPAntonisse/privacy-policy-evaluator) repository.
- **Flask Framework**: This project utilizes the Flask framework for building web applications. We are grateful to the Flask community for their excellent documentation and support.
  **Reclaim hosting and Grinnell College**: This project utilizes hosting support provided through DLAC and reclaim hosting. The documentation provided provided by reclaim hosting for our wsgi.py file and their support was helpful for getting this project on a webserver
