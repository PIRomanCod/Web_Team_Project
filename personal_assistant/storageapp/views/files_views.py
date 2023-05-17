from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from storageapp.services.file_services import FileServices
from storageapp.models import File


class FileViews:

    services = FileServices


    @login_required
    def show_user_files(request):
        return FileViews.services.render_files_list(request)

    @login_required
    def delete_file_warning(request, file_id):

        file = File.objects.get(id=file_id)
        return render(request, 'storageapp/deleting_warning.html', context={'file': file})

    @login_required
    def delete_file(request, file_id):

        if request.method == 'POST':
            file = File.objects.get(id=file_id)
            message = FileViews.services.delete_file(file=file)

            return FileViews.services.render_files_list(request, message=message)
        return FileViews.services.render_files_list(request)
    
    @login_required
    def upload_file(request):

        if request.method == 'POST':
            if not request.FILES.get('file'):
                return render(request, 'storageapp/upload_file.html')

            dropbox_file_name = FileViews.services.save_file_dropbox_and_get_new_name(request)

            owner_inst, type_inst, extension_inst, file_name = FileViews.services.get_file_info(request)

            File.objects.create(owner=owner_inst,
                                file_type=type_inst,
                                file_extension=extension_inst,
                                file_name=file_name,
                                dropbox_file_name=dropbox_file_name)

            return FileViews.services.render_files_list(request)
        return render(request, 'storageapp/upload_file.html')

    @login_required
    def download_file(request, file_id):

        if request.method == 'POST':

            file = File.objects.get(id=file_id)
            url = FileViews.services.download_file(file)

            return redirect(to=url)

        return FileViews.services.render_files_list(request)


    @login_required
    def search_by_name(request):

        word = request.GET.get('user_input')
        message = f'Search result for "{word}":'

        search_result = File.objects.filter(owner=request.user.id).filter(file_name__contains=word)

        if not search_result:
            message = f'I cant find something with "{word}"'

        return FileViews.services.render_files_list(request, files_list=search_result, message=message)
