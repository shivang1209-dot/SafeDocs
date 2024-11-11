# SafeDocs

SafeDocs is a privacy-focused web application designed to securely analyze and extract Personally Identifiable Information (PII) from digital documents, such as PDFs and images, while ensuring data security and compliance.

## Features

- **Comprehensive PII Detection**  
  SafeDocs automatically identifies and extracts sensitive information, including:
  - Names
  - Dates of Birth
  - Aadhaar Numbers
  - PAN Numbers
  - Addresses
  - Virtual ID (VID)

- **Enhanced Security Measures**  
  SafeDocs supports password-protected files, ensuring that sensitive data is analyzed securely without compromising user privacy.

- **Accurate Data Extraction and Formatting**  
  With advanced OCR (Optical Character Recognition) and custom regular expressions, SafeDocs cleans and validates extracted data to match specific Indian ID formats (e.g., Aadhaar, VID) and structured addresses.

- **Streamlined Workflow for Compliance**  
  SafeDocs offers a user-friendly interface, ideal for both individuals and organizations aiming to manage PII securely, supporting privacy compliance and auditing tasks.

## Tech Stack

- **Frontend**: React
- **Backend**: Python (Flask)
- **Database**: MongoDB
- **OCR**: pytesseract with preprocessing for enhanced accuracy

## How It Works

1. **Upload Document**: SafeDocs accepts PDFs and images, including those with complex formats or images embedded.
2. **OCR and Extraction**: Text is extracted using OCR, and PII is identified based on predefined patterns and formats.
3. **Post-Processing**: Extracted text is processed to clean and validate PII fields (e.g., Aadhaar, VID, addresses).
4. **Results**: Extracted PII is displayed in a secure, structured format, allowing users to review and manage data effectively.

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
