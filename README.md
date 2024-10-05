# **DocSafeSIH Django Project**

This repository contains a Django project called **DocSafeSIH**. This README will guide you through the setup and installation process, as well as provide instructions for running the project on your local machine.

## **Table of Contents**
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Project](#running-the-project)
5. [Testing](#testing)
6. [Additional Notes](#additional-notes)

---

## **Overview**

DocSafeSIH is a document security application designed to ensure the privacy and integrity of personal documents. Built using the Django framework, this project allows for secure storage, document validation, and privacy-compliant practices.

---

## **Prerequisites**

Before running the project, ensure you have the following installed on your local machine:

- **Python**: Version 3.6 or higher. You can download Python [here](https://www.python.org/downloads/).
- **Django**: Version 3.0 or higher. It will be installed as part of the project dependencies.
- **Git**: To clone the repository.

---

## **Installation**

To set up and run the Django project on your local environment, follow these steps:

### 1. **Clone the Repository**
Open your terminal (or command prompt) and clone the repository using Git:
```bash
git clone https://github.com/AnkurGarg07/DocSafeSIH.git
```

### 2. **Navigate to the Project Directory**
After cloning, move into the project directory:
```bash
cd DocSafeSIH
```

### 3. **Create and Activate Virtual Environment**

It’s recommended to use a virtual environment to avoid dependency conflicts. To create and activate a virtual environment:

- **Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. **Install Dependencies**
With the virtual environment activated, install all necessary project dependencies:
```bash
pip install -r requirements.txt
```

This command installs all the Python packages required to run the project, as listed in `requirements.txt`.

---

## **Running the Project**

Once the environment is set up, you can now run the Django project locally.

### 1. **Apply Database Migrations**
Before starting the server, apply the migrations to set up your database schema:
```bash
python manage.py migrate
```

### 2. **Start the Development Server**
To start the Django development server, use:
```bash
python manage.py runserver
```

By default, the server will run on `http://localhost:8000/`. Open this URL in your web browser to access the project.

---

## **Testing**

You can run the automated tests that come with the project to ensure everything is working properly. To do this, execute the following command:
```bash
python manage.py test
```

This will run all test cases and display the results in your terminal.

---

## **Additional Notes**

- **Admin Panel**:  
  If the project includes Django's admin functionality, you can access the admin interface at `http://localhost:8000/admin/`. Ensure you’ve created a superuser by running:
  ```bash
  python manage.py createsuperuser
  ```

- **Static Files**:  
  To collect all static files for production, run:
  ```bash
  python manage.py collectstatic
  ```

- **Troubleshooting**:  
  If you encounter any issues during installation or while running the project, refer to the Django [official documentation](https://docs.djangoproject.com/en/3.0/) or seek assistance from project contributors by opening an issue on GitHub.

---

## **Contributing**

We welcome contributions from the community! Feel free to fork this repository, make improvements, and submit a pull request. 

For major changes, please open an issue first to discuss what you'd like to change.

---
