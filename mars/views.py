from django.shortcuts import render
from mars.models import Album, Artist
from django.utils.html import format_html
import markdown
from utils import get_site_cfg, get_site_setup


def get_default_og_image():
    cfg = get_site_cfg()
    setup = get_site_setup()
    return setup.site_root.strip('/') + cfg.header_image.url


def home(request):
    albums = Album.objects.all()
    cfg = get_site_cfg()
    setup = get_site_setup()
    context = {
        **cfg.__dict__,
        **setup.__dict__,
        'og_image': get_default_og_image,
        'albums': albums
    }
    return render(request, 'mars/index.html', context)


def shop(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
        'og_image': get_default_og_image,
    }
    return render(request, 'mars/shop.html', context)


def artist(request, slug):
    artist = Artist.objects.get(slug=slug)
    setup = get_site_setup()
    context = {
        'artist': artist,
        'og_image': setup.site_root.strip('/') + artist.albums.first().image.url
    }
    return render(request, 'mars/artist.html', context)


def album(request, slug):
    album = Album.objects.get(slug=slug)
    setup = get_site_setup()
    context = {
        'album': album,
        'other_albums': album.artist.albums.exclude(id=album.id),
        'og_image': setup.site_root.strip('/') + album.image.url
    }
    return render(request, 'mars/album.html', context)


def about(request):
    cfg = get_site_cfg()
    context = {
        **cfg.__dict__,
        'about_text': format_html(markdown.markdown(cfg.about_text)),
        'og_image': get_default_og_image
    }
    return render(request, 'mars/about.html', context)
