from django.contrib import admin

from .models import FileTypes, FileExtensions, File

# Register your models here.
admin.site.register(FileTypes)
admin.site.register(FileExtensions)
admin.site.register(File)