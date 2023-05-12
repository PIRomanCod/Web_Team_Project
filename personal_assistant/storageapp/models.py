from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class FileTypes(models.Model):

    name = models.CharField(max_length=255)

class FileExtensions(models.Model):

    name = models.CharField(max_length=255)
    category = models.ForeignKey(FileTypes, on_delete=models.CASCADE, default=1)

class File(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.ForeignKey(FileTypes, on_delete=models.CASCADE)
    file_extension = models.ForeignKey(FileExtensions, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    dropbox_file_name = models.CharField(max_length=255, null=True)
    file_url = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

