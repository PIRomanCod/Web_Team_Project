from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image
class FileTypes(models.Model):

    name = models.CharField(max_length=255)
    img = models.ImageField(default='icons/other.jpeg')

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.img.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.img.path)
class FileExtensions(models.Model):

    name = models.CharField(max_length=255)
    category = models.ForeignKey(FileTypes, on_delete=models.CASCADE, default=1)

class File(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.ForeignKey(FileTypes, on_delete=models.CASCADE)
    file_extension = models.ForeignKey(FileExtensions, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    dropbox_file_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_fields_list(cls):
        return {num: field.name for num, field in enumerate(cls._meta.fields) if field.name != 'owner'}

