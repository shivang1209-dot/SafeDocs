from django import forms
from .models import uploadedFile
class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = uploadedFile
        fields = ['file']