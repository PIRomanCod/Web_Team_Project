from django.urls import path
from . import views

app_name = 'contactsapp'

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.create_contact, name='create_contact'),
    path('<int:pk>/edit/', views.edit_contact, name='edit_contact'),
    path('<int:pk>/delete/', views.delete_contact, name='delete_contact'),
    path('search/', views.search_contacts, name='search_contacts'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
]
