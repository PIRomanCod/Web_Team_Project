"""
The forms module contains the forms for the contactapp app.
"""
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    The ContactForm class is a ModelForm for the Contact model.
    """
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d',
                                                                        attrs={'placeholder': 'year-mount-day'})
    )

    class Meta:
        """
        The Meta class defines the model and fields for the ContactForm.
        """
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birth_date']