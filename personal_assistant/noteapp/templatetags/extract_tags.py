from django import template

register = template.Library()


def tags(value):
    # value == note.tags
    return ', '.join([str(name) for name in value.all()])


register.filter('tags', tags)
