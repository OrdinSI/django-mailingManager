from django import template

register = template.Library()


@register.simple_tag()
def blog_image_tags(data):
    if data:
        return f'/media/{data}'
    return '#'
