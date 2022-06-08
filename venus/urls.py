from utils import path
from venus import views


app_name = 'venus'
urlpatterns = (
    # server_path('admin/', admin.site.urls),distill_path
    *path('', views.home),
    *path('cats', views.cats),
    *path('about', views.about)
)
