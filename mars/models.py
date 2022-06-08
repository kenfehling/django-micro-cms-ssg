from django.db import models
from django.template.defaultfilters import slugify
from all.models import BaseSiteConfiguration


class SiteConfiguration(BaseSiteConfiguration):
    subtitle = models.CharField(max_length=64)
    header_image = models.ImageField(upload_to='static/mars/uploads')
    about_text = models.TextField()


class ModelWithSlug(models.Model):
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.__str__())
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


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
