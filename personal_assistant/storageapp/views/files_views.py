from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from storageapp.services.file_services import FileServices
from storageapp.models import File


class FileViews:
    """
    This class contains views for files.
    """

    services = FileServices

    @login_required
    def show_user_files(request):
        """
        The show_user_files function is a view that renders the user's files list.
        It takes in a request object and returns an HttpResponse object with the rendered template.

        :param request: Get the current user, and then pass it to the render_files_list function in fileviews
        :return: render files_list.html in FileServices.render_files_list() with incoming data
        """

        return FileViews.services.render_files_list(request)

    @login_required
    def delete_file_warning(request, file_id):
        """
        The delete_file_warning function is called when the user clicks on the &quot;Delete&quot; button in
        the file_detail.html template.  The function takes a request and a file_id as parameters,
        and returns an HTML response that renders the deleting_warning.html template with context
        containing the File object whose id matches that of the passed-in file_id parameter.

        :param request: Get the request object, which contains information about the current web request
        :param file_id: Get the file object from the database
        :return: render the deleting_warning.html with the context
        """

        file = File.objects.get(id=file_id)
        return render(request, 'storageapp/deleting_warning.html', context={'file': file})

    @login_required
    def delete_file(request, file_id):
        """
        The delete_file function is called when the user clicks on the delete button
        on a file. It takes in a request and an id of the file to be deleted, then it
        gets that file from the database and calls services.delete_file() to delete it.
        It then returns files_list which is rendered by render_files_list().


        :param request: Get the request object, which is used to access information about the current http request
        :param file_id: Identify the file to be deleted
        :return: render files_list.html in FileServices.render_files_list() with incoming data
        """

        if request.method == 'POST':
            file = File.objects.get(id=file_id)
            message = FileViews.services.delete_file(file=file)

            return FileViews.services.render_files_list(request, message=message)
        return FileViews.services.render_files_list(request)

    @login_required
    def upload_file(request):
        """
        The upload_file function is responsible for handling the POST request that comes from the upload_file.html page
        when a user submits a file to be uploaded. The function first checks if there is actually a file attached to the
        request, and if not it renders an empty upload_file.html page so that users can try again with another file. If there
        is indeed a file attached, then we call save_file_dropbox() in services which saves the submitted file into our Dropbox
        account and returns its new name (which will be used later when we create an instance of File). We also get some other info

        :param request: Get the file from the request
        :return: render files_list.html in FileServices.render_files_list() with incoming data
        """

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
        """
        The download_file function is called when the user clicks on a file in the list of files.
        It takes in a request and an id for the file to be downloaded, then it gets that file from
        the database and calls download_file() from services.py to get its url, which is returned as
        a redirect.

        :param request: Get the request object, which is used to check if the method is post
        :param file_id: Identify the file that is to be downloaded
        :return: A redirect to the url of the file if the request method is 'POST'.
                 Otherwise, it renders the file list.
        """

        if request.method == 'POST':
            file = File.objects.get(id=file_id)
            url = FileViews.services.download_file(file)

            return redirect(to=url)

        return FileViews.services.render_files_list(request)

    @login_required
    def search_by_name(request):
        """
        The search_by_name function searches for files by name.
        It takes a request object as an argument and returns the result of the search_by_name function from
        FileViews.services module.

        :param request: Get the user input from the search bar
        :return: render files_list.html in FileServices.render_files_list() with incoming data
        """

        word = request.GET.get('user_input')
        message = f'Search result for "{word}":'

        search_result = File.objects.filter(owner=request.user.id).filter(file_name__contains=word)

        if not search_result:
            message = f'I cant find something with "{word}"'

        return FileViews.services.render_files_list(request, files_list=search_result, message=message)
