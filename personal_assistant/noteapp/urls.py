from django.urls import path
from . import views

app_name = "noteapp"

urlpatterns = [
    path('', views.main, name="main"),
    path('tag/', views.tag, name="tag"),
    path('note/', views.note, name="note"),
    path('detail/<int:note_id>', views.detail, name="detail"),
    path('done/<int:note_id>', views.set_done, name="set_done"),
    path('delete/<int:note_id>', views.delete_note, name="delete"),
]
