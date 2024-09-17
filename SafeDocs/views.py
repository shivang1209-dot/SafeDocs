from django.contrib.auth.decorators import login_required
import os
from .document_process import extract_details, extract_text_from_pdf
from django.shortcuts import render, redirect
from document_processing.forms import PDFUploadForm


def home(request):

    form = PDFUploadForm()

    processed_data = [
        {
            "fileUrl": "https://www.google.com",
            "fileName": "File 1.pdf",
        },
        {
            "fileUrl": "https://www.google.com",
            "fileName": "File 2.pdf",
        },
        {
            "fileUrl": "https://www.google.com",
            "fileName": "File 3.pdf",
        },
        {
            "fileUrl": "https://www.google.com",
            "fileName": "File 4.pdf",
        }
    ]

    return render(request, 'home.html', {'processed_files': processed_data, 'form': form})


@login_required
def results(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save()  # Save the uploaded PDF file
            pdf_path = uploaded_pdf.file.path  # Get the file path

            ocr_text = extract_text_from_pdf(pdf_path)
            details = [extract_details(ocr_text)]


            # print(details)

            # details = [{'Name': 'Himanshu Sharma', 'DOB': '05/08/2005', 'Gender': 'MALE', 'Mobile No': '9873630131', 'Aadhaar Number': '3153 0222 6881', 'VID': '9192 7505 5446 7963', 'Address': 'S/O Praveen Sharma, HOUSE NO. 3261 A, STREET NO. 4, RAGHUBAR PURA NO. 2, GANDHI NAGAR, East Delhi, Delhi - 110031', "Father's Name": 'Praveen Sharma', 'Area PIN Code': '110031'}]

            return render(request, 'results.html', {"processedData": details})
    else:
        return redirect('home')
    
@login_required
def redact(request):
    pass



def dashboard(request,user_name):
    return render(request,"dashboard.html")