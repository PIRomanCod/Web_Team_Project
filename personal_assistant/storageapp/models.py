"""
This module contains the models for the storageapp app.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image


class FileTypes(models.Model):
    """
    This class represents the file types model.
    """
    name = models.CharField(max_length=255)
    img = models.ImageField(default='icons/other.jpeg')

    def save(self, *args, **kwargs):
        """
        The save function is a built-in function that saves the image to the database.
        The super() function allows us to access methods from parent class, in this case,
        the save method of the Model class. The img variable opens up our image file and
        stores it as an Image object. We then check if either height or width of our image
        is greater than 100 pixels and if so we resize it using thumbnail() method which takes a tuple as an argument with new dimensions for our resized image.

        :param self: Refer to the current instance of the class
        :param args: Send a non-keyworded variable length argument list to the function
        :param kwargs: Pass keyworded, variable-length argument list to a function
        :return: The save method of the super class
        :doc-author: Trelent
        """
        super().save()

        img = Image.open(self.img.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.img.path)


class FileExtensions(models.Model):
    """
    This class represents the file extensions model.
    """
    name = models.CharField(max_length=255)
    category = models.ForeignKey(FileTypes, on_delete=models.CASCADE, default=1)


class File(models.Model):
    """
    This class represents the file model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.ForeignKey(FileTypes, on_delete=models.CASCADE)
    file_extension = models.ForeignKey(FileExtensions, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    dropbox_file_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
