"""
The module forms is used to create forms for the models. The forms are used in the module views.
"""

from django.forms import ModelForm, CharField, TextInput, Textarea, Form
from . import models


class TagForm(ModelForm):
    """
    The TagForm is used to create a form for the Tag model.
    """
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput(attrs={"class": "test_class"}))

    class Meta:
        model = models.Tag
        fields = ['name']


class NoteForm(ModelForm):
    """
    The NoteForm is used to create a form for the Note model.
    """
    name = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=Textarea(attrs={"rows": "3"}))

    class Meta:
        model = models.Note
        fields = ['name', 'description']
        exclude = ['tags']


class NoteSearchForm(Form):
    """
    The NoteSearchForm is used to create a form for the Note model.
    """
    keyword = CharField(max_length=100, required=False, widget=TextInput(attrs={'placeholder': 'Search'}))

    def search(self, queryset):
        """
        The search function takes a queryset and returns the same queryset, but filtered by keyword.
            The search function is called in the view with:
            form = SearchForm(request.GET)
            if form.is_valid():
            query = form.search(query)

        :param self: Refer to the class itself, in this case it is used to access the cleaned_data dictionary
        :param queryset: Filter the results
        :return: A queryset which is the result of filtering the original queryset
        """
        keyword = self.cleaned_data.get('keyword')
        if keyword:
            queryset = queryset.filter(name__icontains=keyword) | queryset.filter(description__icontains=keyword)
        return queryset