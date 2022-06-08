from django.db import models
from all.models import BaseSiteConfiguration

class SiteConfiguration(BaseSiteConfiguration):
    subtitle = models.CharField(max_length=64)
    header_image = models.ImageField(upload_to='static/venus/uploads')
    about_text = models.TextField()


class Cat(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='static/venus/uploads/cats')

    def __str__(self):
        return self.name
