"""
    The module models.py is used to create the models of the application.

    It contains the following class:
    - Profile: The class Profile is used to create the model of the profile. After creating the models, we need to migrate them to the database.

    To do this, we need to run the following commands:
    - python manage.py makemigrations
    - python manage.py migrate
"""
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    """
    The class Profile is used to create the model of the profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default_avatar.png', upload_to='profile_images')

    def __str__(self):
        """
        The __str__ function is the default human-readable representation of the object.
        This function will be called whenever you call str() on an object which uses this model,
        or in several other similar situations (such as displaying an object in the Django admin site).
        It should return a string representing the thing you want to see when that happens.

        :param self: Represent the instance of the class
        :return: The username of the user
        """
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        """
        The save function is a built-in function that saves the model instance to the database.
            The save method takes optional keyword arguments that are passed to the save() method of
            the underlying model class. The default implementation does nothing.

        :param self: Refer to the current instance of a class
        :param args: Send a non-keyworded variable length argument list to the function.
        :param kwargs: Pass keyworded, variable-length argument list to a function.
        :return: The object that is being saved
        """
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
