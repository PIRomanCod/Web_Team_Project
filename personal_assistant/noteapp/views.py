from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import TagForm, NoteForm, NoteSearchForm
from .models import Tag, Note


def main(request):
    tag = request.GET.get('tag')
    if tag:
        notes = Note.objects.filter(tags__name__icontains=tag).filter(user=request.user).order_by('id').all()
    else:
        notes = Note.objects.filter(user=request.user).order_by('id').all()
    paginator = Paginator(notes, 10)  # пагинация по 10 объектов на странице
    page_obj = paginator.get_page(request.GET.get('page'))
    tags = Tag.objects.all()
    return render(request, 'noteapp/index.html', {'page_obj': page_obj, 'tags': tags})



@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="noteapp:main")
        else:
            return render(request, 'noteapp/tag.html', context={'form': form})

    return render(request, 'noteapp/tag.html', context={'form': TagForm()})


@login_required
def note(request):
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
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/detail.html', context={"note": note})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to="noteapp:main")


@login_required
def set_active(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=False)
    return redirect(to="noteapp:main")


@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to="noteapp:main")


@login_required
def search(request):
    form = NoteSearchForm(request.GET)
    keyword = request.GET.get('keyword', None)
    notes = Note.objects.filter(user=request.user).all()
    if keyword:
        notes = notes.filter(name__icontains=keyword)|notes.filter(description__icontains=keyword)
    return render(request, 'search.html', {'form': form, 'notes': notes})


@login_required
def update_note(request, note_id):
    """
    Updated on May 13th, 2023 to include the ability to update notes.
    """
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            note.tags.set(choice_tags)

            return redirect(to="noteapp:detail", note_id=note_id)
        else:
            return render(request, 'noteapp/update_note.html', context={'form': form})

    return render(request, 'noteapp/update_note.html', context={'form': NoteForm(instance=note), 'note_id': note_id})

