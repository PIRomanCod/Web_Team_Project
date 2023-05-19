"""
This module contains the FileServices class.
"""

import re
from django.shortcuts import render
from django.contrib.auth.models import User
from storages.backends.dropbox import DropBoxStorage

from storageapp.models import File, FileTypes, FileExtensions


class FileServices:
    """
    This class contains methods for working with files.
    """

    reg_ex_extension = r'\.[^./\\]+$'
    dbx_storage = DropBoxStorage()

    @classmethod
    def get_file_info(cls, request):
        """
        The get_file_info function is a class method that takes in the request object and returns
        the owner instance, type instance, extension instance and file name. The function first gets the
        file from the request object. It then gets the user id from the request user to get an owner
        instance of that user. Next it checks if there is a value for 'user_input' in POST data which would be
        the case when renaming files or folders (see rename_file()). If there is no value for 'user_input', then we use
        the original file name as our file name variable. We also check if

        :param cls: Pass the class of the model to be created
        :param request: Get the file from the request
        :return: A tuple with the following information:
        """
        file = request.FILES.get('file')
        owner_inst = User.objects.get(id=request.user.id)
        user_file_name = request.POST.get('user_input')

        try:
            extension = re.findall(cls.reg_ex_extension, file.name)[0]
            extension_inst = FileExtensions.objects.get(name=extension)

        except FileExtensions.DoesNotExist:
            extension_inst = FileExtensions.objects.get(id=1)

        type_inst = extension_inst.category
        file_name = user_file_name if user_file_name else file.name

        return owner_inst, type_inst, extension_inst, file_name

    @classmethod
    def save_file_dropbox_and_get_new_name(cls, request):
        """
        The save_file_dropbox_and_get_new_name function saves a file to Dropbox and returns the new name of the file.

        :param cls: Refer to the class that is being used
        :param request: Get the file from the request
        :return: The name of the file that was saved to dropbox
        """
        file = request.FILES.get('file')

        dropbox_file_name = cls.dbx_storage.save(file.name, file)
        return dropbox_file_name

    @classmethod
    def delete_file(cls, file):

        """
        The delete_file function takes a file object as an argument and deletes it from the database.
        It also deletes the file from Dropbox, using the dropbox_file_name attribute of that object.

        :param cls: Specify the class that is being used to call the function
        :param file: Identify the file to be deleted
        :return: The string 'file {name} deleted'
        """
        name = file.file_name
        cls.dbx_storage.delete(file.dropbox_file_name)
        file.delete()
        return f'File >{name}< deleted'

    @classmethod
    def download_file(cls, file):

        """
        The download_file function takes a file object as an argument and returns the url of that file.
        The function uses the dropbox_storage class to get the url of a given file.

        :param cls: Pass the class to a method
        :param file: Find the file in the database
        :return: The url of the file
        """
        url = cls.dbx_storage.url(file.dropbox_file_name)
        return url

    @staticmethod
    def render_files_list(request, files_list=None, message='This is your files.'):

        """
        The render_files_list function is used to render the files_list.html template, which displays a list of all
        files belonging to the user who is currently logged in. The function takes two arguments: request and
        files_list, which are both required for rendering the template. The optional message argument can be used
        to display a custom message on top of the page.

        :param request: Pass the request object to the function
        :param files_list: Pass the list of files to be displayed
        :param message: Pass a message to the user
        :return: A rendered storageapp/files_list.html template with the context
        """

        fields = {'file_type': 'Type', 'file_extension': 'Extension', 'file_name': 'File Name',
                  'created_at': 'Created at'}
        all_files_types = [f_type.name for f_type in FileTypes.objects.all()]

        if not request.GET.getlist('filter_type'):
            files_types_enabled = all_files_types
        else:
            files_types_enabled = request.GET.getlist('filter_type')

        field_to_order = request.GET.get('category') if request.GET.get('category') else 'file_name'
        order_rules = f'-{field_to_order}' if '-' in files_types_enabled else field_to_order

        files_types_obj = [FileTypes.objects.get(name=name) for name in files_types_enabled if name != '-']

        if files_list:
            return render(request, 'storageapp/files_list.html', context={'files_list': files_list,
                                                                          'files_types_enabled': files_types_enabled,
                                                                          'file_fields': fields,
                                                                          'all_files_types': all_files_types,
                                                                          'message': message})

        files_list = (File.objects.filter(owner=request.user.id)
                      .filter(file_type__in=files_types_obj)
                      .order_by(order_rules))

        return render(request, 'storageapp/files_list.html', context={'files_list': files_list,
                                                                      'files_types_enabled': files_types_enabled,
                                                                      'file_fields': fields,
                                                                      'all_files_types': all_files_types,
                                                                      'message': message})
