from django.shortcuts import render
from all.models import SiteSetup
from venus.models import Cat, SiteConfiguration
from django.utils.html import format_html
import markdown


def get_site_cfg():
    return SiteConfiguration.objects.first()


def get_site_setup():
    return SiteSetup.objects.filter(site='venus').first()


def get_default_og_image():
    cfg = get_site_cfg()
    setup = get_site_setup()
    return setup.site_root.strip('/') + cfg.header_image.url


def home(request):
    cats = Cat.objects.all()
    cfg = get_site_cfg()
    setup = get_site_setup()
    context = {
        **cfg.__dict__,
        **setup.__dict__,
        'cats': cats,
        'og_image': get_default_og_image(),
    }
    return render(request, 'venus/index.html', context)


def cats(request):
    cats = Cat.objects.all()
    context = {
        'cats': cats,
        'og_image': get_default_og_image(),
    }
    return render(request, 'venus/cats.html', context)


def about(request):
    cfg = get_site_cfg()
    context = {
        **cfg.__dict__,
        'about_text': format_html(markdown.markdown(cfg.about_text)),
        'og_image': get_default_og_image()
    }
    return render(request, 'venus/about.html', context)
