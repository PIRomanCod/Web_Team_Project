from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d',
                                                                        attrs={'placeholder': 'year-mount-day'})
    )

    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birth_date']
