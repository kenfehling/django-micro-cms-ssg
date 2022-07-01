from django.db import models
from all.models import BaseSiteConfiguration, ModelWithSlug


class SiteConfiguration(BaseSiteConfiguration):
    subtitle = models.CharField(max_length=64)
    header_image = models.ImageField(upload_to='static/mars/uploads')
    about_text = models.TextField()


class Artist(ModelWithSlug):
    name = models.CharField(max_length=200)
    link = models.URLField()
    country = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Album(ModelWithSlug):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/mars/uploads/albums')
    link = models.URLField()
    album_id = models.CharField("Album ID (Bandcamp)", max_length=64, unique=True)

    def __str__(self):
        return f'{self.artist.name} - {self.title}'
