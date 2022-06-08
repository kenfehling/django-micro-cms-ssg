from django.contrib import admin
from django.urls import include, path
from . import views
import os
from config import SITES

site = os.getenv('SITE')
public_root = os.environ.get('PUBLIC_ROOT', '')

if site is None:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.home),
        *[path(s + '/', include(f'{s}.urls')) for s in SITES]
    ]
else:
    urlpatterns = [
        path(public_root, include(site + '.urls'))
    ]
