"""
The module forms is used to create forms for the models. The forms are used in the views.py file.
"""


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput, ModelForm, ImageField, FileInput

from .models import Profile


class RegisterForm(UserCreationForm):
    """
    The class RegisterForm is used to create a form for the User model
    """
    username = CharField(max_length=100,
                         required=True,
                         widget=TextInput())
    first_name = CharField(max_length=150, required=False, widget=TextInput(attrs={"class": "form-control"}))
    last_name = CharField(max_length=150, required=False, widget=TextInput(attrs={"class": "form-control"}))
    email = EmailField(max_length=150, required=True, widget=EmailInput(attrs={"class": "form-control"}))
    password1 = CharField(max_length=50,
                          required=True,
                          widget=PasswordInput())
    password2 = CharField(max_length=50,
                          required=True,
                          widget=PasswordInput())

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    """
    The class LoginForm is used to create a form for the User model.
    """
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(ModelForm):
    """
    The class ProfileForm is used to create a form for the Profile model.
    """
    avatar = ImageField(widget=FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']
