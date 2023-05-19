"""
    The module view is content the functions that will be called when the user types the url.
    The view function will return a response to the user.
    The response can be a html page.
    The view function can also call other functions to process the request.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import TagForm, NoteForm, NoteSearchForm
from .models import Tag, Note


def main(request):
    """
    The main function is the main page of the noteapp.
    It displays all notes and tags, as well as a pagination system.

    :param request: Get the request object
    :return: The rendered index
    """
    tag = request.GET.get('tag')
    if tag:
        notes = Note.objects.filter(tags__name__icontains=tag).filter(user=request.user).order_by('id').all()
    else:
        notes = Note.objects.filter(user=request.user).order_by('id').all()
    paginator = Paginator(notes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    tags = Tag.objects.all()
    return render(request, 'noteapp/index.html', {'page_obj': page_obj, 'tags': tags})


@login_required
def tag(request):
    """
    The tag function is used to create a new tag.
        It takes in the request and returns a redirect to the note page if successful,
        or renders an error message if not.

    :param request: Get the request object
    :return: The tag
    """
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="noteapp:note")
        else:
            return render(request, 'noteapp/tag.html', context={'form': form})

    return render(request, 'noteapp/tag.html', context={'form': TagForm()})


@login_required
def note(request):
    """
    The note function is used to create a new note.
        It takes the request as an argument and returns a rendered template with the form for creating notes.
        If the method of request is POST, then it checks if form data is valid and saves it in database.
        Then it adds tags to this note from choice_tags list (choice_tags contains all tags that were chosen by user).

    :param request: Get the user from the request
    :return: The form for creating a new note
    """
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags:
                note.tags.add(tag)

            return redirect(to="noteapp:main")
        else:
            return render(request, 'noteapp/note.html',  context={'form': form, 'tags': tags})

    return render(request, 'noteapp/note.html', context={'form': NoteForm(), 'tags': tags})


@login_required
def detail(request, note_id):
    """
    The detail function is used to display a single note.
    It takes the request and the id of the note as parameters,
    and returns an HTML page with that specific note.

    :param request: Get the current user
    :param note_id: Find the specific note that is being requested
    :return: A view with the note that was requested
    """
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/detail.html', context={"note": note})


@login_required
def set_done(request, note_id):
    """
    The set_done function takes a request and note_id as parameters.
    It then filters the Note objects by the primary key of note_id, and only returns those that belong to the user making
    the request. It then updates those notes field "done"=True.
    Finally, it redirects to the main noteapp page.

    :param request: Get the user from the request object
    :param note_id: Find the note in the database
    :return: The redirect function, which returns an http response redirect object
    """
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to="noteapp:main")


@login_required
def set_active(request, note_id):
    """
    The set_active function takes a request and note_id as parameters.
    It then filters the Note objects by the primary key of note_id, and updates it to be active (done=False).
    Finally, it redirects to the main noteapp page.

    :param request: Get the user that is currently logged in
    :param note_id: Find the note that is being updated
    :return: The redirect function, which
    """
    Note.objects.filter(pk=note_id, user=request.user).update(done=False)
    return redirect(to="noteapp:main")


@login_required
def delete_note(request, note_id):
    """
    The delete_note function takes in a request and note_id, then deletes the Note object with that id.
    It redirects to the main noteapp page.

    :param request: Get the user who is logged in
    :param note_id: Find the note to delete
    :return: A redirect to the main page
    """
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to="noteapp:main")


@login_required
def search(request):
    """
    The search function takes a request and returns a rendered search.html template with the form, notes, and keyword
        variables passed to it. The function first creates an instance of NoteSearchForm using the request's GET data as
        its argument. It then assigns the value of 'keyword' in that same GET data to a variable called keyword (or None if
        there is no such key). Next, it queries all notes belonging to the user making this request and assigns them to
        another variable called notes. If there is indeed a value for keyword in our GET data (i.e., if someone has entered

    :param request: Get the current request object, which contains all of the information about the current http request
    :return: A list of notes that match the search term
    """
    form = NoteSearchForm(request.GET)
    keyword = request.GET.get('keyword', None)
    notes = Note.objects.filter(user=request.user).all()
    if keyword:
        notes = notes.filter(name__icontains=keyword) | notes.filter(description__icontains=keyword)
    return render(request, 'search.html', {'form': form, 'notes': notes})


@login_required
def update_note(request, note_id):
    """
    The update_note function is responsible for updating a note.
    It takes in the request and the id of the note to be updated as parameters.
    The function first gets the note object from Note model using get_object_or_404 method, which returns an error if no such object exists.
    Then it checks whether there is a POST request or not, and if so, it creates a form instance with that data and saves it to database after checking its validity.
    If there was no POST request then we just render an empty form.

    :param request: Get the request from the user
    :param note_id: Get the note that we want to update
    :return: A redirect to the detail view
    """
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    tags = note.tags.all()

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            note.tags.set(tags)

            return redirect(to="noteapp:detail", note_id=note_id)
        else:
            return render(request, 'noteapp/update_note.html', context={'form': form})

    return render(request, 'noteapp/update_note.html', context={'form': NoteForm(instance=note), 'note_id': note_id})

