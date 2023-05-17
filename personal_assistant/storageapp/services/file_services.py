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

        type_inst = extension_inst.category
        file_name = user_file_name if user_file_name else file.name

        return owner_inst, type_inst, extension_inst, file_name

    @classmethod
    def save_file_dropbox_and_get_new_name(cls, request):
        file = request.FILES.get('file')

        dropbox_file_name = cls.dbx_storage.save(file.name, file)
        return dropbox_file_name

    @classmethod
    def delete_file(cls, file):
        name = file.file_name
        cls.dbx_storage.delete(file.dropbox_file_name)
        file.delete()
        return f'File >{name}< deleted'

    @classmethod
    def download_file(cls, file):

        url = cls.dbx_storage.url(file.dropbox_file_name)
        return url

    @staticmethod
    def render_files_list(request, files_list=None, message='This is your files.'):


        fields = {'file_type': 'Type', 'file_extension': 'Extension', 'file_name': 'File Name', 'created_at': 'Created at'}
        all_files_types = [type.name for type in FileTypes.objects.all()]

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
