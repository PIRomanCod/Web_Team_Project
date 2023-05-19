"""
The models module contains the Contact model.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Contact(models.Model):
    """
    The Contact model contains the following fields:
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(r'^\d{5,15}$', 'Enter a valid phone number.'
                                                ' Min lenght is 5, max lenght is 15, only numbers.')
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    email = models.EmailField(blank=True)
    birth_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        """
        The __str__ function is used to return a string representation of the object.
        This is useful for debugging and also for displaying objects in the shell.

        :param self: Represent the instance of the class
        :return: The name of the object
        """
        return self.name