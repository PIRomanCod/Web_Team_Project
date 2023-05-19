"""
    The module view is contents the function that will be called when the user types the url.
    The view function will return a response to the user.
    The response can be a html page.
    The view function can also call other functions to process the request.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm


def signupuser(request):
    """
    The signupuser function is a view that handles the signup process for users.
        If the user is already authenticated, they are redirected to the main page.
        If not, and if it's a POST request (i.e., if they've submitted their information),
        then we check whether or not their form data was valid;
        if so, we save it and redirect them to the main page; otherwise, we render an error message.

    :param request: Get the request from the client
    :return: A redirect to the root page if the user is authenticated
    """
    if request.user.is_authenticated:
        return redirect(to='root') # redirect to main page if user is authenticated

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='root') # redirect to main page if user is authenticated
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    """
    The loginuser function is a view that handles the login of users.
        It checks if the user is already authenticated, and if so redirects them to the main page.
        If not, it checks whether or not they are using POST data (i.e., submitting a form).
        If they are, it authenticates their username and password against Django's built-in authentication system.

    :param request: Get the request object from the view
    :return: A redirect to the root page if the user is authenticated
    """
    if request.user.is_authenticated:
        return redirect('root') # redirect to main page if user is authenticated

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='root') # redirect to main page if user is authenticated

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    """
    The logoutuser function logs out the user and redirects them to the root page.

    :param request: Get the current user
    :return: A redirect to the root url
    """
    logout(request)
    return redirect(to='root') # redirect to main page if user is authenticated


@login_required
def profile(request):
    """
    The profile function is used to update the user's profile.
        It takes a request as an argument and returns a render of the users/profile.html template
        with the profile_form variable passed in.

    :param request: Get the request object from the user
    :return: A rendered html page with the profile form
    """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
