from urllib import parse
from django.shortcuts import render

from storageapp.services.file_services import FileServices
from storageapp.models import File


class FileViews:

    @staticmethod
    def show_user_files(request):

        files_list = FileServices.get_user_files_list(user_id=request.user.id)

        return render(request, 'storageapp/files_list.html', context={'files_list': files_list})

    @staticmethod
    def delete_file_warning(request, file_id):
        file = File.objects.get(id=file_id)
        return render(request, 'storageapp/deleting_warning.html', context={'file': file})

    @staticmethod
    def delete_file(request, file_id):
        if file_id:
            file = File.objects.get(id=file_id)
            FileServices.delete_file(file=file)

        files_list = FileServices.get_user_files_list(user_id=request.user.id)
        return render(request, 'storageapp/files_list.html', context={'files_list': files_list})


    @staticmethod
    def upload_file(request):
        if request.method == 'POST':
            file_url, dropbox_file_name = FileServices.save_file_dropbox_and_get_url(request)
            owner_inst, type_inst, extension_inst, file_name = FileServices.get_info_from_file(request)
            File.objects.create(owner=owner_inst,
                                file_type=type_inst,
                                file_extension=extension_inst,
                                file_name=file_name,
                                file_url=file_url,
                                dropbox_file_name=dropbox_file_name)
            return render(request, 'storageapp/upload_file.html')
        return render(request, 'storageapp/upload_file.html')
