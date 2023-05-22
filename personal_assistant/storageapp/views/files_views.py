import logging

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views import View

from storageapp.services.file_services import FileServices, FileTypes
from storageapp.models import File



class FilesListView(ListView):
    model = File
    template_name = 'storageapp/files_list.html'


    def get_queryset(self):

        all_files_types, files_types_enabled, file_fields = FileServices.get_filter_and_sort_rules(self.request)

        field_to_order = self.request.GET.get('category', 'file_name')
        order_rules = f'-{field_to_order}' if '-' in files_types_enabled else field_to_order

        files_list = (File.objects.filter(owner=self.request.user.id)
                      .filter(file_type__in=[FileTypes.objects.get(name=name) for name in files_types_enabled if name != '-'])
                      .order_by(order_rules))

        return files_list

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_files_types'], context['files_types_enabled'], context['file_fields'] = \
            FileServices.get_filter_and_sort_rules(self.request)

        context.setdefault('message', 'Your files')
        context.setdefault('title', 'My files')

        return context

class FileUploadView(View):
    template_name = 'storageapp/upload_file.html'

    @method_decorator(login_required())
    def get(self, request):
        return render(request, self.template_name, context={'title': 'Upload'})

    @method_decorator(login_required())
    def post(self, request):

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

class FileDeleteWarningView(TemplateView):
    template_name = 'storageapp/deleting_warning.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file = File.objects.get(id=self.kwargs['file_id'])
        context['file'] = file
        context['title'] = 'Deleting'
        return context


class FileDeleteView(View):

    @method_decorator(login_required())
    def post(self, request, file_id):
        file = File.objects.get(id=file_id)
        FileServices.delete_file(file)
        return redirect('storageapp:files_list')


class FileDownloadView(View):

    @method_decorator(login_required())
    def post(self, request, file_id):
        file = File.objects.get(id=file_id)
        url = FileServices.download_file(file)
        return redirect(to=url)

class SearchByNameView(View):

    @method_decorator(login_required())
    def get(self, request):

        word = request.GET.get('user_input')
        message = f'Search result for "{word}":'

        search_result = File.objects.filter(owner=request.user.id).filter(file_name__contains=word)

        if not search_result:
            message = f'I cant find something with "{word}"'

        return FilesListView.as_view(
            template_name='storageapp/files_list.html',
            extra_context={'object_list': search_result, 'message': message, 'title': 'Search Files'}
        )(request)




