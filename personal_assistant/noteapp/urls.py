from django.urls import path
from . import views

app_name = "noteapp"

urlpatterns = [
    path('search/', views.search, name="search"),
    path('', views.main, name="main"),
    path('tag/', views.tag, name="tag"),
    path('note/', views.note, name="note"),
    path('detail/<int:note_id>', views.detail, name="detail"),
    path('done/<int:note_id>', views.set_done, name="set_done"),
    path('active/<int:note_id>', views.set_active, name="set_active"),
    path('delete/<int:note_id>', views.delete_note, name="delete"),
    path('update_note/<int:note_id>', views.update_note, name="update_note"),

]
