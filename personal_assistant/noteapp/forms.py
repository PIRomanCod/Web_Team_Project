from django.forms import ModelForm, CharField, TextInput, Form
from . import models


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput(attrs={"class": "test_class"}))

    class Meta:
        model = models.Tag
        fields = ['name']


class NoteForm(ModelForm):
    name = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = models.Note
        fields = ['name', 'description']
        exclude = ['tags']


class NoteSearchForm(Form):
    keyword = CharField(max_length=100, required=False, widget=TextInput(attrs={'placeholder': 'Search'}))

    def search(self, queryset):
        keyword = self.cleaned_data.get('keyword')
        if keyword:
            queryset = queryset.filter(name__icontains=keyword) | queryset.filter(description__icontains=keyword)
        return queryset