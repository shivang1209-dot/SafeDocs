from django.db import models
from django.contrib.auth.models import User
class uploadedFile(models.Model):
    file = models.FileField(upload_to='documents/')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)



class redactedFile(models.Model):
    file = models.FileField(upload_to='redactedFile/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=255,default="null")
    processed_path = models.CharField(max_length=255,default="null")
    uploaded_at = models.DateTimeField(auto_now_add=True)

