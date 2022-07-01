from django.shortcuts import render
from utils import get_site_cfg, get_site_setup
from .models import Post
from django.utils.html import format_html


def _format_post(p):
    return {**p.__dict__, 'text': format_html(p.text)}


def _get_posts():
    return [_format_post(p) for p in Post.objects.all()]


def posts(request):
    cfg = get_site_cfg()
    setup = get_site_setup()
    context = {
        **cfg.__dict__,
        **setup.__dict__,
        'posts': _get_posts()
    }
    return render(request, 'blog/posts.html', context)


def post(request, slug):
    context = {
        'post':_format_post(Post.objects.get(slug=slug))
    }
    return render(request, 'blog/post.html', context)


def home(request):
    cfg = get_site_cfg()
    context = {
        **cfg.__dict__,
        'posts': _get_posts()
    }
    return render(request, 'blog/index.html', context)
