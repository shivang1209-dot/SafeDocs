from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import render, redirect
from document_processing.forms import PDFUploadForm
import mimetypes
from django.core.exceptions import ValidationError
# from .image_process import extract_text_from_image, extract_details_from_text, get_sensitive_data_boxes, redact_image
from PIL import Image
from .document_process import extract_details, extract_text_from_pdf, mask_sensitive_data_in_pdf
from django.http import FileResponse, Http404
from django.conf import settings
from document_processing.models import redactedFile


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


def results(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save the uploaded PDF file
            file_path = uploaded_file.file.path
            print(file_path)  # Get the file path
            file_name = os.path.basename(file_path)
            print("This is file name", file_name)

            mime_type, _ = mimetypes.guess_type(file_path)

            # Supported file types
            supported_types = ['application/pdf', 'image/jpeg', 'image/png']

            if mime_type not in supported_types:
                uploaded_file.delete()
                return render(request, 'upload.html', {'error': 'Unsupported file type. Please upload a PDF, JPEG, JPG, or PNG file.'})

            if mime_type == 'application/pdf':
                ocr_text, doc = extract_text_from_pdf(file_path)
                details = extract_details(ocr_text)
                if (request.user.is_authenticated):
                        masked_pdf_path = mask_sensitive_data_in_pdf(
                            doc, details, file_name)
                        redacted_file = redactedFile(file=uploaded_file.file,
                                                     original_name=file_name,
                                                     processed_path=masked_pdf_path,
                                                     user=request.user)
                        redacted_file.save()

                        print(masked_pdf_path)
                        if os.path.exists(file_path):
                            os.remove(file_path)

                # elif mime_type in ['image/jpeg', 'image/png']:
                #     image = Image.open(file_path).convert("RGB")
                #     extracted_text, ocr_results = extract_text_from_image(image)
                #     details = [extract_details_from_text(extracted_text)]

            return render(request, 'results.html', {"processedData": details, "file_name": file_name})
    else:
        return redirect('home')


@login_required
def redact(request):
    return render(request, "dashboard.html")


@login_required
def dashboard(request, user_name):
    return render(request, "dashboard.html")


@login_required
def download_redacted_file(request, filename):
    # Define the file path
    file_path = os.path.join(
        settings.MEDIA_ROOT, 'redactedFile/'+filename)

    # Check if file exists
    if not os.path.exists(file_path):
        raise Http404("File not found")

    # Return the file as a downloadable response
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
