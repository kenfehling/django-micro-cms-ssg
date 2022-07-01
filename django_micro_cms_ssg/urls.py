from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django_micro_cms_ssg import settings
from . import views
import os
from config import SITES

site = os.getenv('SITE')
public_root = os.environ.get('PUBLIC_ROOT', '')

if site is None:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('summernote/', include('django_summernote.urls')),
        path('', views.home),
        *[path(s + '/', include(f'{s}.urls')) for s in SITES]
    ]
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = [
        path(public_root, include(site + '.urls'))
    ]
