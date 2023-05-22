"""
        The module models.py is used to create the models of the noteapp application.

        It contains the following classes:
        - Tag: The class Tag is used to create the model of the tag.
        - Note: The class Note is used to create the model of the note.
        After creating the models, we need to migrate them to the database.
        To do this, we need to run the following commands:
        - python manage.py makemigrations
        - python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    The class Tag is used to create the model of the tag in the database.
    """
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    The class Note is used to create the model of the note in the database.
    """
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
