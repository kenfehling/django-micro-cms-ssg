from mars import views
from mars.models import Album, Artist
from utils import path


def artist_gen():
    for a in Artist.objects.all():
        yield {'slug': a.slug}


def album_gen():
    for a in Album.objects.all():
        yield {'slug': a.slug}

app_name = 'mars'
urlpatterns = (
    *path('', views.home),
    *path('shop', views.shop),
    *path('about', views.about),
    *path('artist/<str:slug>', views.artist, distill_func=artist_gen),
    *path('album/<str:slug>', views.album, distill_func=album_gen),
)
