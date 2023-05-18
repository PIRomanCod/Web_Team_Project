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
    The class Tag is used to create the model of the tag.
    """
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        """
        The Meta class is used to specify model-specific options.
        """
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        """
        The __str__ function is used to return a string representation of the object.
        This is useful for debugging and also for displaying objects in the shell.

        :param self: Refer to the current instance of the class, and is used to access variables that belongs to the class
        :return: The name of the tag
        :doc-author: Trelent
        """
        return self.name


class Note(models.Model):
    """
    The class Note is used to create the model of the note.
    """
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        """
        The __str__ function is used to return a string representation of the object.
        This is useful for debugging and also for displaying objects in the shell.

        :param self: Represent the instance of the class
        :return: The article/name of the note
        :doc-author: Trelent
        """
        return self.name
