from django.urls import path
from .views.files_views import FileViews
app_name = 'storageapp'

urlpatterns = [
    path('upload_file/', FileViews.upload_file, name='upload_file'),
    path('files_list/', FileViews.show_user_files, name='files_list'),
    path('delete_file_warning/<int:file_id>', FileViews.delete_file_warning, name='delete_file_warning'),
    path('delete_file/<int:file_id>', FileViews.delete_file, name='delete_file')
]