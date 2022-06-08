import random
from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.urls import resolve
from sorl.thumbnail import get_thumbnail
import os

register = template.Library()

def get_app_name(context):
    return resolve(context.request.path_info).func.__module__.split('.')[0]

@register.filter
def as_abs_url(path, request):
    return request \
        .build_absolute_uri(path) \
        .replace('testserver', 'localhost:8000')  # TODO: Make flexible.

@register.filter
def file(path):
    return open(path[1:], 'rb')

@register.simple_tag()
def img(path, size, format=None, **kwargs) -> str:
    public_root = os.environ.get('PUBLIC_ROOT', '')
    if path.startswith('/'):
        path = path[1:]  # Make /static/... -> static/...
    with open(path, 'rb') as f:
        if format is None:
            format = path.split('.')[-1].upper()
        return f'{public_root}{get_thumbnail(path, size, format=format, **kwargs)}'

@register.simple_tag()
def picture(path, size, alt, style=None, className=None, **kwargs) -> str:
    return format_html(f"""
    <picture>
        <source srcset="/{img(path, size, 'WEBP', **kwargs)}" type="image/webp" />
        <source srcset="/{img(path, size, 'PNG', **kwargs)}" type="image/png" />
        <img src="/{img(path, size, 'PNG', **kwargs)}" loading="lazy" alt="{alt}", style="{style}" class="{className}" />
    </picture>
    """)


@register.simple_tag(takes_context=True)
def link(context, href):
    return reverse(get_app_name(context) + ':' + href)


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp
