"""
This module contains command for create files types and files extensions in FileExtension and FileTypes tables from storageapp
"""
from django.core.management.base import BaseCommand
from storageapp.services.create_tables import create_tables


class Command(BaseCommand):
    """
    This class contains command for create files types and files extensions in FileExtension and FileTypes tables from storageapp
    """
    help = 'Command create files types and files extensions in FileExtension and FileTypes tables from storageapp'

    def handle(self, *args, **options):
        """
        The handle function is the entry point for a Django management command.
        It's called by the manage.py script when you run python manage.py &lt;command&gt;
        from your project directory.

        :param self: Represent the instance of the class
        :param args: Pass a variable number of arguments to a function
        :param options: Pass in the options that are passed to the command
        :return: A string that is printed in the console
        :doc-author: Trelent
        """
        create_tables()
