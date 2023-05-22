"""
The views module contains functions that define what should happen when a user visits a certain URL.
"""
from datetime import date, timedelta
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Contact
from .forms import ContactForm


@login_required
def contact_list(request):
    """
    The contact_list function is a view that displays all contacts in the database.
    It uses the Django Paginator class to paginate results, and it passes those results
    to the contact_list.html template for rendering.
    Decorator login_required is used to ensure that only logged-in users can access this view.
    Function contact_list returns only contacts that belong to the user who made this request.

    :param request: Get the current user
    :return: The contact_list
    """
    contacts = Contact.objects.filter(user=request.user).order_by('name')
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_contacts = paginator.get_page(page_number)
    return render(request, 'contactapp/contact_list.html', {'contacts': page_contacts, 'title': 'Contact list'})


@login_required
def create_contact(request):
    """
    The create_contact function is a view that allows the user to create a new contact.
    The function first checks if the request method is POST, which means that the form has been submitted.
    If it's not POST, then we're creating a blank form for them to fill out and render it in our template.
    If it's POST, then we take data from our bound form (form) and save it to our database.
    Decorator login_required is used to ensure that only logged-in users can access this view.
    Function create_contact add the current logged-in user to the contact object before saving it to database.

    :param request: Get the request from the browser
    :return: A response
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contactapp:contact_list')
    else:
        form = ContactForm()
    return render(request, 'contactapp/create_contact.html', context={'form': form, 'title': 'Create contact'})


@login_required
def edit_contact(request, pk):
    """
    The edit_contact function takes a request and primary key (pk) as arguments.
    It gets the contact object with the given pk, or returns a 404 error if it doesn't exist.
    If the request method is POST, we instantiate ContactForm with the submitted data and also pass
    in instance=contact so Django populates ContactForm with values from an existing model instance.
    If form is valid, we save it to database and redirect user to contact list page;
    otherwise render edit_contact template passing in form variable for displaying validation errors (if any).
    If request method is GET, we instantiate ContactForm without any data passed in so

    :param request: Pass the request object to the view
    :param pk: Get the contact object from the database
    :return: A form to edit the contact
    """
    contact = get_object_or_404(Contact, id=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contactapp:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contactapp/edit_contact.html', {'form': form, 'contact': contact, 'title': 'Edit contact'})


@login_required
def delete_contact(request, pk):
    """
    The delete_contact function is a view that allows the user to delete a contact.
    The function takes in two arguments: request and pk. The request argument is an HTTP
    request object, while the pk argument represents the primary key of a Contact object.
    The function first gets an instance of Contact with id equal to pk and user equal to
    the current logged-in user (or returns 404 if no such instance exists). If this is
    a POST request, then it deletes the contact and redirects back to the list of contacts;
    otherwise, it renders 'contactapp/delete_contact.html

    :param request: Get the request object
    :param pk: Identify the contact to be deleted
    :return: The delete_contact
    """
    contact = get_object_or_404(Contact, id=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contactapp:contact_list')
    return render(request, 'contactapp/delete_contact.html', {'contact': contact, 'title': 'Delete contact'})


@login_required
def search_contacts(request):
    """
    The search_contacts function takes a request object as an argument and returns a rendered template.
    The function first gets the search_query from the GET data of the request object,
    then it filters all contacts that belong to the user who made this request.
    Then it filters those contacts by name, address, phone number, email or birthdate if any of these fields contain
    the search query string (case insensitive).
    The filtered results are passed into context dictionary along with the original search query string.
    Finally we render 'search_contacts' template using this context.

    :param request: Get the search query from the url
    :return: A rendered template
    """
    search_query = request.GET.get('search_query', '')
    user_contacts = Contact.objects.filter(user=request.user)
    search_results = user_contacts.filter(
        models.Q(name__icontains=search_query) |
        models.Q(address__icontains=search_query) |
        models.Q(phone_number__icontains=search_query) |
        models.Q(email__icontains=search_query) |
        models.Q(birth_date__icontains=search_query)
    )

    context = {
        'search_query': search_query,
        'search_results': search_results,
        'title': 'Search contacts'
    }

    return render(request, 'contactapp/search_contacts.html', context)


@login_required
def upcoming_birthdays(request):
    """
    The upcoming_birthdays function takes a request and returns an HTML page with the contacts that have birthdays
    within the next x days (in 0 - 365 interval), where x is specified by the user. The function first checks if it has received a POST request.
    If so, it gets the number of days from this POST request and converts it to an integer (if possible). It then creates
    a date object for today's date and another one for end_date = current_date + timedelta(days=x). It initializes result
    to be an empty list. Then, it iterates through all of its user's contacts in order to find those whose

    :param request: Get the request object
    :return: A list of contacts that have birthdays in the next x days
    """
    if request.method == 'POST':
        days = request.POST.get('days', 0)
        days = int(days) if days else 0
        current_date = date.today()
        end_date = current_date + timedelta(days=days)

        result = []

        contacts = Contact.objects.filter(user=request.user)
        for contact in contacts:
            if contact.birth_date:
                birthday_date = date(year=date.today().year, month=contact.birth_date.month, day=contact.birth_date.day)
                birthday_date_next_year = date(year=date.today().year + 1, month=contact.birth_date.month,
                                               day=contact.birth_date.day)
                if date.today() < birthday_date <= end_date or date.today() < birthday_date_next_year <= end_date:
                    result.append(contact)

    else:
        result = []

    return render(request, 'contactapp/upcoming_birthdays.html', {'contacts': result, 'title': 'Upcoming Birthdays'})