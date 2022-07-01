from django.db import models
from all.models import BaseSiteConfiguration, ModelWithSlug


class SiteConfiguration(BaseSiteConfiguration):
    subtitle = models.CharField(max_length=64)
    header_image = models.ImageField(upload_to='static/blog/uploads')
    about_text = models.TextField()


class Post(ModelWithSlug):
    title = models.CharField(max_length=512)
    text = models.TextField()

    def __str__(self):
        return self.title
