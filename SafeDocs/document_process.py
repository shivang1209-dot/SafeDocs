import pymupdf
import re

def extract_text_from_pdf(pdf_path, password=None):
    text = ""
    try:
        doc = pymupdf.open(pdf_path)
        if password and not doc.authenticate(password):
            return "Incorrect password provided."
        
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_details(text):
    details = {
        'Name': None,
        'DOB': None,
        'Gender': None,
        'Mobile No': None,
        'Aadhaar Number': None,
        'VID': None,
        'Address': None,
        'Father\'s Name': None,
        'Area PIN Code': None
    }

    # Define regex patterns
    name_pattern = re.compile(r'\b([A-Z][a-z]+\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b')
    dob_pattern = re.compile(r'DOB:\s*\b\d{2}/\d{2}/\d{4}\b')
    gender_pattern = re.compile(r'\b(MALE|FEMALE|OTHER)\b', re.IGNORECASE)
    mobile_pattern = re.compile(r'\b\d{10}\b')
    aadhar_pattern = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')
    
    # Updated VID pattern to capture only the 16-digit number
    vid_pattern = re.compile(r'VID[^0-9]*([\d\s]{4}\s[\d\s]{4}\s[\d\s]{4}\s[\d\s]{4})', re.IGNORECASE)
    
    # Address pattern to start with 'Address:' and end with 6-digit PIN code
    address_pattern = re.compile(
        r'Address\s*:\s*([\s\S]*?\d{6})',
        re.DOTALL
    )

    # Extract DOB
    dob_match = dob_pattern.search(text)
    if dob_match:
        details['DOB'] = dob_match.group(0).replace("DOB:", "").strip()

        # Extract the name line which is immediately above the DOB line
        dob_index = text.index(dob_match.group(0))
        before_dob_text = text[:dob_index].strip()
        name_lines = before_dob_text.split('\n')
        
        if len(name_lines) > 1:
            possible_name_line = name_lines[-2].strip()  # Line immediately above DOB
            name_match = name_pattern.search(possible_name_line)
            if name_match:
                details['Name'] = name_match.group(0)

    # Extract Gender
    gender_match = gender_pattern.search(text)
    if gender_match:
        details['Gender'] = gender_match.group(0).upper()

    # Extract Mobile Number
    mobile_match = mobile_pattern.search(text)
    if mobile_match:
        details['Mobile No'] = mobile_match.group(0)

    # Extract Aadhaar Number
    aadhar_match = aadhar_pattern.search(text)
    if aadhar_match:
        details['Aadhaar Number'] = aadhar_match.group(0)

    # Extract VID
    vid_match = vid_pattern.search(text)
    if vid_match:
        details['VID'] = vid_match.group(1).strip()

    # Extract Address and Father's Name
    address_match = address_pattern.search(text)
    if address_match:
        address_text = address_match.group(1).strip()
        # Extract PIN code from address text
        pin_code_match = re.search(r'\d{6}', address_text)
        if pin_code_match:
            details['Address'] = address_text[:pin_code_match.end()].strip()
            details['Area PIN Code'] = pin_code_match.group(0)

        # Extract Father's Name from address text
        father_name_match = re.search(r'S/O\s*\s*([A-Za-z\s]+),', address_text) or re.search(r'C/O:\s*\s*([A-Za-z\s]+),', address_text)
        if father_name_match:
            details['Father\'s Name'] = father_name_match.group(1).strip()

    return details