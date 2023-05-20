from django import template
from django.db.models import Count

from ..models import Tag

register = template.Library()


def tags(value):
    """
    The tags function takes a note's tags and returns them as a comma-separated list.
    It is used in the templates because Tag is a ManyToManyField and cannot be accessed directly.


    :param value: Pass the note
    :return: A string of all the tags for a note
    """
    return ', '.join([str(name) for name in value.all()])


def toptags(request):
    return Tag.objects.annotate(num_notes=Count('note')).order_by('-num_notes')[:5]



register.filter('tags', tags)
register.filter('toptags', toptags)
