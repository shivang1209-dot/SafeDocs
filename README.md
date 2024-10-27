# Django Project Readme

This readme file provides instructions on how to run the Django project on your system.

## Prerequisites
Before running the project, make sure you have the following installed:
- Python (version 3.6 or higher)
- Django (version 3.0 or higher)

## Installation
1. Clone the project repository to your local machine.
`git clone https://github.com/AnkurGarg07/DocSafeSIH.git`
2. Open a terminal or command prompt and navigate to the project directory.
3. Create a virtual environment by running the command: `python -m venv .venv`
4. Activate the virtual environment:
    - On Windows: `.venv\Scripts\activate`
    - On macOS/Linux: `source .venv/bin/activate`
5. Install the project dependencies by running: `pip install -r requirements.txt`


## Running the Project
1. Run the following command to apply the database migrations: `python manage.py migrate`
2. Start the development server by running: `python manage.py runserver`
3. Open your web browser and navigate to `http://localhost:8000` to access the project.

## Additional Notes
- If you encounter any issues during the installation or running of the project, refer to the project documentation or seek help from the project contributors.
