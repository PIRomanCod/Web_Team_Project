from django.core.management.base import BaseCommand
from storageapp.services.create_tables import create_tables
class Command(BaseCommand):
    help = 'Command create files types and files extensions in FileExtension and FileTypes tables from storageapp'

    def handle(self, *args, **options):
        create_tables()
