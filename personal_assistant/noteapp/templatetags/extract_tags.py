from django import template

register = template.Library()


def tags(value):
    """
    The tags function takes a note's tags and returns them as a comma-separated list.
    It is used in the templates because Tag is a ManyToManyField and cannot be accessed directly.


    :param value: Pass the note
    :return: A string of all the tags for a note
    :doc-author: Trelent
    """
    return ', '.join([str(name) for name in value.all()])


register.filter('tags', tags)
