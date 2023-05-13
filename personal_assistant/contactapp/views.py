from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Contact
from .forms import ContactForm


@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user).order_by('name')
    paginator = Paginator(contacts, 10)  # Показувати не більше 10 контактів на сторінці
    page_number = request.GET.get('page')
    page_contacts = paginator.get_page(page_number)
    return render(request, 'contact_list.html', {'contacts': page_contacts})


@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'create_contact.html', {'form': form})


@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'edit_contact.html', {'form': form, 'contact': contact})


@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'delete_contact.html', {'contact': contact})


@login_required
def search_contacts(request):
    search_query = request.GET.get('search_query', '')
    search_results = Contact.objects.filter(
        models.Q(name__icontains=search_query) |
        models.Q(address__icontains=search_query) |
        models.Q(phone_number__icontains=search_query) |
        models.Q(email__icontains=search_query) |
        models.Q(birth_date__icontains=search_query)
    )

    context = {
        'search_query': search_query,
        'search_results': search_results
    }

    return render(request, 'search_contacts.html', context)


@login_required
def upcoming_birthdays(request):
    if request.method == 'POST':
        days = int(request.POST.get('days', 0))
        end_date = timezone.now() + timedelta(days=days)
        contacts = Contact.objects.filter(birth_date__range=[timezone.now(), end_date])
    else:
        contacts = []

    return render(request, 'upcoming_birthdays.html', {'contacts': contacts})
