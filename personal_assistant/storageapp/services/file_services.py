import re
from django.shortcuts import render
from django.contrib.auth.models import User
from storages.backends.dropbox import DropBoxStorage

from storageapp.models import File, FileTypes, FileExtensions


class FileServices:
    reg_ex_existance = r'\.[^./\\]+$'
    dbx_storage = DropBoxStorage()

    @classmethod
    def get_file_info(cls, request):
        file = request.FILES.get('file')
        owner_inst = User.objects.get(id=request.user.id)
        user_file_name = request.POST.get('user_input')

        try:
            extension = re.findall(cls.reg_ex_existance, file.name)[0]
            extension_inst = FileExtensions.objects.get(name=extension)

        except FileExtensions.DoesNotExist:
            extension_inst = FileExtensions.objects.get(id=1)

        type_inst: FileTypes = extension_inst.category

        if user_file_name:
            file_name = user_file_name
        else:
            file_name = file.name

        return owner_inst, type_inst, extension_inst, file_name

    @classmethod
    def save_file_dropbox_and_get_new_name(cls, request):
        file = request.FILES.get('file')

        dropbox_file_name = cls.dbx_storage.save(file.name, file)
        return dropbox_file_name

    @classmethod
    def delete_file(cls, file):

        cls.dbx_storage.delete(file.dropbox_file_name)
        file.delete()
        return 'File deleted'

    @classmethod
    def download_file(cls, file):

        url = cls.dbx_storage.url(file.dropbox_file_name)
        return url

    @staticmethod
    def render_files_list(request, files_list=None, message='This is your files.'):

        fields_to_order = File.get_fields_list()
        fields_to_choice = {2: 'Type', 3: 'Extension', 4: 'File Name', 6: 'Created at'}

        all_files_types = [type.name for type in FileTypes.objects.all()]

        if not request.GET.getlist('filter_type'):
            files_types_enabled = all_files_types
        else:
            files_types_enabled = request.GET.getlist('filter_type')

        how_order = int(request.GET.get('category')) if request.GET.get('category') else 0
        reverse_order = '-' if '-' in files_types_enabled else ''
        files_types_obj = [FileTypes.objects.get(name=name) for name in files_types_enabled if name != '-']

        if files_list:
            return render(request, 'storageapp/files_list.html', context={'files_list': files_list,
                                                                          'files_types_enabled': files_types_enabled,
                                                                          'file_fields': fields_to_choice,
                                                                          'all_files_types': all_files_types,
                                                                          'message': message})
        files_list = (File.objects.filter(owner=request.user.id)
                      .filter(file_type__in=files_types_obj)
                      .order_by(f'{reverse_order}{fields_to_order[how_order]}'))

        return render(request, 'storageapp/files_list.html', context={'files_list': files_list,
                                                                      'files_types_enabled': files_types_enabled,
                                                                      'file_fields': fields_to_choice,
                                                                      'all_files_types': all_files_types,
                                                                      'message': message})
