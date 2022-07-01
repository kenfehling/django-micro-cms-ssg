from django.contrib import admin
from mars.models import Album, Artist, SiteConfiguration
from solo.admin import SingletonModelAdmin


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
