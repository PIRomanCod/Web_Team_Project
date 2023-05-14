from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from storageapp.services.file_services import FileServices
from storageapp.models import File


class FileViews:

    @staticmethod
    @login_required
    def show_user_files(request):
        return FileServices.render_files_list(request)

    @staticmethod
    def create_tables(request):
        FileServices.create_tables()
        return FileServices.render_files_list(request)

    @staticmethod
    @login_required
    def delete_file_warning(request, file_id):
        file = File.objects.get(id=file_id)
        return render(request, 'storageapp/deleting_warning.html', context={'file': file})

    @staticmethod
    @login_required
    def delete_file(request, file_id):
        if request.method == 'POST':
            file = File.objects.get(id=file_id)
            FileServices.delete_file(file=file)

        return FileServices.render_files_list(request)

    @staticmethod
    @login_required
    def upload_file(request):
        if request.method == 'POST':
            if not request.FILES.get('file'):
                return render(request, 'storageapp/upload_file.html')
            dropbox_file_name = FileServices.save_file_dropbox_and_get_new_name(request)
            owner_inst, type_inst, extension_inst, file_name = FileServices.get_file_info(request)
            File.objects.create(owner=owner_inst,
                                file_type=type_inst,
                                file_extension=extension_inst,
                                file_name=file_name,
                                dropbox_file_name=dropbox_file_name)

            return FileServices.render_files_list(request)
        return render(request, 'storageapp/upload_file.html')

    @staticmethod
    @login_required
    def download_file(request, file_id):
        if request.method == 'POST':
            file = File.objects.get(id=file_id)
            url = FileServices.downlaod_file(file)
            return redirect(to=url)

        return FileServices.render_files_list(request)
