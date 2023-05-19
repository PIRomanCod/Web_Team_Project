"""
    The module signals is used to create signals for the models. The signals are used in the models.py file.
    """
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    The create_profile function is a receiver that gets called via the post_save signal whenever a User object is created.
        It checks if the created user was actually saved to the database (created == True),
        and then creates a corresponding Profile instance.

    :param sender: Specify the model that is being used
    :param instance: Pass the user instance to the profile model
    :param created: Check if the user is created or not
    :param kwargs: Pass keyworded, variable-length argument list
    :return: A profile object
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    The save_profile function is a receiver that handles post_save signals from User instances.
    Whenever a User is created and saved, the function creates an associated Profile
    instance using the create_profile() method we defined earlier.
    Whenever a User instance is updated and saved, it updates its associated Profile.

    :param sender: Specify the model that is sending the signal
    :param instance: Pass the user instance to the save_profile function
    :param kwargs: Pass a variable number of keyword arguments to a function
    :return: Nothing
    """
    instance.profile.save()
