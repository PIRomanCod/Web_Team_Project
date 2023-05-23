from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView


from storageapp.services.decorators import BaseView
from storageapp.services.file_services import FileServices, FileTypes
from storageapp.models import File


class FilesListView(BaseView, ListView):
    """View for displaying a list of files."""

    model = File
    template_name = 'storageapp/files_list.html'

    def get_queryset(self):
        """
        The get_queryset function is used to filter the queryset of files that are displayed in the table.
        The function first gets all file types, and then filters out those that are not enabled by the user.
        Then it orders them according to a field specified by the user.

        :param self: Access the class attributes and methods
        :return: A list of files that are owned by the user
        """
        all_files_types, files_types_enabled, file_fields = FileServices.get_filter_and_sort_rules(self.request)

        field_to_order = self.request.GET.get('category', 'file_name')
        order_rules = f'-{field_to_order}' if '-' in files_types_enabled else field_to_order

        files_list = (File.objects.filter(owner=self.request.user.id)
                      .filter(
                          file_type__in=[FileTypes.objects.get(name=name) for name in files_types_enabled if name != '-'])
                      .order_by(order_rules))

        return files_list

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        The get_context_data function is a method of the ListView class.
        It's purpose is to add additional context variables to the template that will be rendered.
        The function takes in two arguments, self and args, kwargs.
        The self argument refers to the instance of this class ListView.
        The args argument allows for an arbitrary number of positional arguments passed into this function when its called from another location in our codebase.
        This means that we can pass any number of positional arguments into get_context_data() when we call it elsewhere in our codebase and they will all be stored as a tuple inside.

        :param self: Represent the instance of the class
        :param args: Pass an arbitrary number of arguments to a function
        :param object_list: Pass the list of files to be displayed
        :param kwargs: Pass keyworded, variable-length argument list to a function
        :return dict: context for the template
        """
        context = super().get_context_data(**kwargs)

        context['all_files_types'], context['files_types_enabled'], context['file_fields'] = \
            FileServices.get_filter_and_sort_rules(self.request)

        context.setdefault('message', 'Your files')
        context.setdefault('title', 'My files')

        return context


class FileUploadView(BaseView):
    """View for uploading a file."""

    template_name = 'storageapp/upload_file.html'

    @method_decorator(login_required)
    def get(self, request):
        """
        The get function is used to render the upload page.

        :param self: Represent the instance of the object itself
        :param request: Get the request object that is sent to the server
        :return: A render function
        """
        return render(request, self.template_name, context={'title': 'Upload'})

    @method_decorator(login_required)
    def post(self, request):
        """
        The post function is called when the user submits a file to be uploaded.
        The function first checks if there is a file in the request, and if not it returns an error message.
        If there is a file, it calls FileServices' save_file_dropbox_and_get_new name method to upload the
        file to dropbox and get its new name. It then gets information about the owner of the file,
        what type of document it is (e.g., resume), what extension it has (.pdf), and what its original filename was
        and create file-row in DB.

        :param self: Represent the instance of the class
        :param request: Get the file from the post request
        :return: A redirect to the files_list view
        """
        if not request.FILES.get('file'):
            return render(request, self.template_name)

        dropbox_file_name = FileServices.save_file_dropbox_and_get_new_name(request)
        owner_inst, type_inst, extension_inst, file_name = FileServices.get_file_info(request)

        File.objects.create(
            owner=owner_inst,
            file_type=type_inst,
            file_extension=extension_inst,
            file_name=file_name,
            dropbox_file_name=dropbox_file_name
        )

        return redirect('storageapp:files_list')


class FileDeleteWarningView(BaseView, TemplateView):
    """View for displaying a warning before deleting a file."""

    template_name = 'storageapp/deleting_warning.html'

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a function that allows you to pass additional context variables to the template.
        In this case, we are passing the file object and title variable.

        :param self: Refer to the object itself
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A dictionary of data that is used by the template to render the page
        """
        context = super().get_context_data(**kwargs)
        file = File.objects.get(id=self.kwargs['file_id'])
        context['file'] = file
        context['title'] = 'Deleting'
        return context


class FileDeleteView(BaseView):
    """View for deleting a file."""

    @method_decorator(login_required)
    def post(self, request, file_id):
        """
        The post function is used to delete a file from the database.
        It takes in a request and file_id as parameters, then uses the FileServices class to delete the file.
        Finally, it redirects back to files_list.

        :param self: Represent the instance of the object itself
        :param request: Get the request from the client
        :param file_id: Identify the file that needs to be deleted
        :return: A redirect to the files_list view
        """
        file = File.objects.get(id=file_id)
        FileServices.delete_file(file)
        return redirect('storageapp:files_list')


class FileDownloadView(BaseView):
    """View for downloading a file."""

    @method_decorator(login_required)
    def post(self, request, file_id):
        """
        The post function is used to download a file from the server.
        It takes in a request and file_id as parameters, then uses the FileServices class to download the file.
        The function returns a redirect response with url of where the downloaded file is located.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param file_id: Get the file object from the database
        :return: The url of the file
        """
        file = File.objects.get(id=file_id)
        url = FileServices.download_file(file)
        return redirect(to=url)


class SearchByNameView(BaseView):
    """View for searching files by name."""

    @method_decorator(login_required)
    def get(self, request):
        """
        The get function is used to search for files in the database.
        It takes a request object as an argument and returns a view of all files that match the user's input.

        :param self: Represent the instance of the object itself
        :param request: Get the user input from the search bar
        :return: render 'storageapp/files_list.html' with search result
        """
        word = request.GET.get('user_input')
        message = f'Search result for "{word}":'

        search_result = File.objects.filter(owner=request.user.id).filter(file_name__contains=word)

        if not search_result:
            message = f'I can\'t find something with "{word}"'

        return FilesListView.as_view(
            template_name='storageapp/files_list.html',
            extra_context={'object_list': search_result, 'message': message, 'title': 'Search Files'}
        )(request)
