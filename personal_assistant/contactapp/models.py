from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(r'^\d{5,15}$', 'Enter a valid phone number.'
                                                ' Min lenght is 5, max lenght is 15, only numbers.')
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    email = models.EmailField(blank=True)
    birth_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name