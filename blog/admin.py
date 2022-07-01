from django.contrib import admin
from django.db import models
from .models import Post, SiteConfiguration
from solo.admin import SingletonModelAdmin
from django_summernote.admin import SummernoteModelAdmin


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)
