from utils import path
from venus import views


app_name = 'venus'
urlpatterns = (
    *path('', views.home),
    *path('cats', views.cats),
    *path('about', views.about)
)
