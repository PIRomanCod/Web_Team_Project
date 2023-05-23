"""
This module contains all the urls for the storageapp app.
"""
from django.urls import path
from .views.files_views import FilesListView, FileUploadView, FileDeleteView, FileDeleteWarningView, FileDownloadView, SearchByNameView
app_name = 'storageapp'

urlpatterns = [
    path('upload_file/', FileUploadView.as_view(), name='upload_file'),
    path('files_list/', FilesListView.as_view(), name='files_list'),
    path('delete_file_warning/<int:file_id>', FileDeleteWarningView.as_view(), name='delete_file_warning'),
    path('delete_file/<int:file_id>', FileDeleteView.as_view(), name='delete_file'),
    path('download_file/<int:file_id>', FileDownloadView.as_view(), name='download_file'),
    path('search_by_name/', SearchByNameView.as_view(), name='search_by_name'),
]