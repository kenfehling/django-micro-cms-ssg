from django.contrib import admin
from venus.models import Cat, SiteConfiguration
from solo.admin import SingletonModelAdmin


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    pass
