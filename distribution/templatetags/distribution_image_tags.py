from django import template

register = template.Library()


@register.simple_tag()
def catalog_image_tags(data):
    if data:
        return f'/media/{data}'
    return '#'
