from django.contrib import admin
from . import models

admin.site.register(models.uploadedFile)
admin.site.register(models.redactedFile)

# Register your models here.
