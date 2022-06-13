import random
from typing import List
from django import template
from django.urls import reverse
from django.utils.html import format_html, escape
from django.utils.encoding import smart_str
from django.urls import resolve
from sorl.thumbnail import get_thumbnail
import os
import re

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


def img(path, size, format=None, **kwargs) -> str:
    if path.startswith('/'):
        path = path[1:]  # Make /static/... -> static/...
    with open(path, 'rb') as f:
        if format is None:
            format = path.split('.')[-1].upper()
            if format == 'JPG':
                format = 'JPEG'
        return get_thumbnail(path, f'{size.geometry}', format=format, **kwargs)


def create_srcset(path, *sizes, **kwargs) -> List[str]:
    public_root = os.environ.get('PUBLIC_ROOT', '')
    srcs = [f'/{public_root}{img(path, size, **kwargs)}' for size in sizes]
    srcset = [f'{src} {size.width}w' for src, size in zip(srcs, sizes)]
    return srcset


def create_sizes_attr(sizes) -> str:
    # ss = sorted(sizes, key=lambda s: bool(s.min_width), reverse=True)
    return ', '.join([f'(min-width: {size.min_width}) {size.width}px' 
                      for size in sizes if size.min_width is not None])


class SizeNode(template.Node):
    def __init__(self, parser, token):
        bits = token.split_contents()
        self.geometry = str(parser.compile_filter(bits[1]))
        self.min_width = str(parser.compile_filter(bits[2])) if len(bits) > 2 else None

    @property
    def width(self) -> int:
        return int(self.geometry.split('x')[0])


@register.tag
def size(parser, token):
    return SizeNode(parser, token)


kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')


class ImageNode(template.Node):
    def __init__(self, parser, token, nodelist):
        bits = token.split_contents()
        self.path = parser.compile_filter(bits[1])
        self.options = []
        options_bits = bits[2:]
        for bit in options_bits:
            m = kw_pat.match(bit)
            if not m:
                raise template.TemplateSyntaxError(self.error_msg)
            key = smart_str(m.group('key'))
            expr = parser.compile_filter(m.group('value'))
            self.options.append((key, expr))

        self.token = token
        self.nodelist = nodelist

    def render(self, context):
        path = self.path.resolve(context)
        options = {}
        for key, expr in self.options:
            noresolve = {'True': True, 'False': False, 'None': None}
            value = noresolve.get(str(expr), expr.resolve(context))
            if key == 'options':
                options.update(value)
            else:
                options[key] = value
        
        if 'alt' not in options:
            raise Exception("alt is required")

        sizes = [node for node in self.nodelist if isinstance(node, SizeNode)]
        if len(sizes) == 0:
            raise Exception("At least one size is required")

        alt = options.get('alt', '')
        style = options.get('style', '')
        className = options.get('class', '')
        sizes_attr = create_sizes_attr(sizes)
        return format_html(f"""
        <picture>
            <source srcset="{','.join(create_srcset(path, *sizes, format='WEBP', **options))}" sizes="{sizes_attr}" type="image/webp" />
            <source srcset="{','.join(create_srcset(path, *sizes, **options))}" sizes="{sizes_attr}" />
            <img srcset="{','.join(create_srcset(path, *sizes, **options))}" sizes="{sizes_attr}" loading="lazy" alt="{alt}" style="{style}" class="{className}" />
        </picture>
        """)


@register.tag(name="image")
def image(parser, token):
    nodelist = parser.parse(("endimage",))
    parser.delete_first_token()
    return ImageNode(parser, token, nodelist)


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp
