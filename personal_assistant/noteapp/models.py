from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
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
