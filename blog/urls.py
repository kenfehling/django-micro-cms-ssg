from . import views
from .models import Post
from utils import path


def post_gen():
    for a in Post.objects.all():
        yield {'slug': a.slug}


app_name = 'blog'
urlpatterns = (
    *path('', views.home),
    *path('about', views.posts),
    *path('post/<str:slug>', views.post, distill_func=post_gen)
)
