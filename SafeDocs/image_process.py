# import easyocr
# from PIL import Image, ImageDraw, ImageFilter
# import numpy as np
# import re
# import nltk
# from nltk.corpus import words
# import os
# import logging

# logging.getLogger("easyocr").setLevel(logging.ERROR)

# # Download the words corpus if not already available
# nltk.download('words')

# # Load the list of English words
# common_english_words = set(words.words())

# # Function to extract text from an image
# def extract_text_from_image(image):
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(np.array(image))
#     text = ' '.join([text for _, text, _ in result])
#     return text, result

# # Function to extract details from the extracted text
# def extract_details_from_text(text):
#     details = {
#         'Name': None,
#         'DOB': None,
#         'Gender': None,
#         'Mobile No': None,
#         'Aadhaar Number': None,
#         'VID': None,
#         'Address': None,
#         'Father\'s Name': None,
#         'Area PIN Code': None
#     }

#     # Define regex patterns
#     name_pattern = re.compile(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}\b')
#     dob_pattern = re.compile(r'DOB:\s*\d{2}/\d{2}/\d{4}')
#     gender_pattern = re.compile(r'\b(MALE|FEMALE|OTHER)\b', re.IGNORECASE)
#     mobile_pattern = re.compile(r'\b\d{10}\b')
#     aadhar_pattern = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')
#     vid_pattern = re.compile(r'VID[\s:]*([\d\s]{4}\s[\d\s]{4}\s[\d\s]{4}\s[\d\s]{4})', re.IGNORECASE) or re.compile(r'VID[:]*([\d\s]{4}\s[\d\s]{4}\s[\d\s]{4}\s[\d\s]{4})', re.IGNORECASE)
#     address_pattern = re.compile(r'Address\s*:*\s*([\s\S]*?\d{6})', re.DOTALL)

#     # Extract DOB
#     dob_match = dob_pattern.search(text)
#     if dob_match:
#         details['DOB'] = dob_match.group(0).replace("DOB:", "").strip()

#         # Extract the 30 characters before DOB
#         dob_index = text.index(dob_match.group(0))
#         text_before_dob = text[:dob_index].strip()[-30:]  # Get last 30 characters before DOB

#         # Extract Name from the 30 characters substring
#         name_matches = name_pattern.findall(text_before_dob)
#         if name_matches:
#             # Choose the most likely name based on length
#             possible_name = max(name_matches, key=len)
#             # Split the name into words and filter out common English words
#             name_words = possible_name.split()
#             filtered_name = ' '.join(word for word in name_words if word.lower() not in common_english_words)
#             # Update the name in details if it's not empty
#             if filtered_name:
#                 details['Name'] = filtered_name

#     # Extract Gender
#     gender_match = gender_pattern.search(text)
#     if gender_match:
#         details['Gender'] = gender_match.group(0).upper()

#     # Extract Mobile Number
#     mobile_match = mobile_pattern.search(text)
#     if mobile_match:
#         details['Mobile No'] = mobile_match.group(0)

#     # Extract Aadhaar Number
#     aadhar_match = aadhar_pattern.search(text)
#     if aadhar_match:
#         details['Aadhaar Number'] = aadhar_match.group(0)

#     # Extract VID
#     vid_match = vid_pattern.search(text)
#     if vid_match:
#         details['VID'] = vid_match.group(1).strip()

#     # Extract Address and Area PIN Code
#     address_match = address_pattern.search(text)
#     if address_match:
#         address_text = address_match.group(1).strip()
#         # Extract PIN Code from address text
#         pin_code_match = re.search(r'\d{6}', address_text)
#         if pin_code_match:
#             details['Address'] = address_text[:pin_code_match.end()].strip()
#             details['Area PIN Code'] = pin_code_match.group(0)

#     # Extract Father's Name
#     address_start_index = text.find('Address')
#     if address_start_index != -1:
#         address_text = text[address_start_index:]
#         father_name_match = re.search(r'S/O\s*[:]*\s*([A-Za-z\s]+),', address_text)
#         if father_name_match:
#             details['Father\'s Name'] = father_name_match.group(1).strip()

#     return details

# # Function to identify sensitive data in OCR results for redaction
# def get_sensitive_data_boxes(ocr_results):
#     sensitive_data_boxes = []

#     for result in ocr_results:
#         bbox, text = result[0], result[1]
#         if not bbox or len(bbox) != 4:
#             continue  # Skip invalid bounding boxes

#         # Extract bounding box coordinates
#         x_min = min([point[0] for point in bbox])
#         y_min = min([point[1] for point in bbox])
#         x_max = max([point[0] for point in bbox])
#         y_max = max([point[1] for point in bbox])

#         if re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text):
#             # Calculate partial bounding box for the first 8 digits
#             text_width = ((x_max - x_min) * (7/10))  # Approximate width for 8 digits
#             partial_bbox_coords = (x_min, y_min, x_min + text_width, y_max)
#             sensitive_data_boxes.append((partial_bbox_coords, text[:8]))  # Add first 8 digits

#         if re.search(r'VID[^0-9]*([\d\s]{4}\s[\d\s]{4}\s[\d\s]{4}\s[\d\s]{4})', text):
#             text_width = ((x_max - x_min) * (4/5))  # Approximate width for 12 digits
#             partial_bbox_coords = (x_min, y_min, x_min + text_width, y_max)
#             sensitive_data_boxes.append((partial_bbox_coords, text[:12]))  # Add first 12 digits

#     return sensitive_data_boxes

# # Function to redact the sensitive data in the image
# def redact_image(image, sensitive_data):
#     draw = ImageDraw.Draw(image)

#     for bbox_coords, text in sensitive_data:
#         x_min, y_min, x_max, y_max = bbox_coords
#         if x_min >= x_max or y_min >= y_max:
#             continue  # Skip invalid regions

#         # Apply a stronger blur to the area containing the first 8 digits for Aadhaar and 12 digits for VID
#         blurred_region = image.crop((x_min, y_min, x_max, y_max)).filter(ImageFilter.GaussianBlur(20))
#         image.paste(blurred_region, (x_min, y_min))

#     return image

# # Function to save the redacted image
# def save_redacted_image(image, output_path):
#     image.save(output_path)
#     print(f"Redacted image saved as {output_path}")

# # Function to process the image, extract details, and redact sensitive data
# def process_image(image_path):
#     image = Image.open(image_path).convert("RGB")

#     # Extract text and OCR results from image
#     extracted_text, ocr_results = extract_text_from_image(image)

#     # Extract details from the text
#     details = extract_details_from_text(extracted_text)
#     print("Extracted Details:\n")
#     for key, value in details.items():
#         print(f"{key}: {value if value else 'Not found'}")

#     # Identify sensitive data for redaction
#     sensitive_data = get_sensitive_data_boxes(ocr_results)

#     if sensitive_data:
#         redacted_image = redact_image(image, sensitive_data)
#         if redacted_image:
#             # Ensure the output path is correctly formatted
#             base, ext = os.path.splitext(image_path)
#             output_path = f'{base}_redacted{ext}'
#             save_redacted_image(redacted_image, output_path)
#     else:
#         print("No sensitive data found. No redaction applied.")

