from django.db import models
from solo.models import SingletonModel
from datetime import datetime, timezone
from django.template.defaultfilters import slugify

_help_style = 'line-height:1.15rem'

class SiteSetup(models.Model):
    site = models.CharField(
        "Site (name of Django app)",
        max_length=32, db_index=True, unique=True,
        editable=False)
    git_repo = models.CharField(
        "Git repository (for automatic git push)",
        help_text=f"""
            <div style='{_help_style}'>
                <b>git@github.com:&lt;username&gt;/&lt;repo&gt</b>
                or whatever you'd use with git clone.<br />
                If you've set up an SSH key and use Git over SSH, everything should work.
            </div>
        """,
        max_length=2048, null=True, blank=True)
    site_root = models.URLField(
        "Root URL of the production site", 
        help_text=f"""
            <div style='{_help_style}'>
                Usually something like <b>https://yourdomain.com</b><br />
                Recommended but optional unless the site is served from a subdirectory.<br />
                Also useful for certain meta tags.
            </div>
        """,
        null=True, blank=True)
    auto_publish_wait = models.PositiveSmallIntegerField(
        "Auto publish after last update (minutes)",
        help_text=f"""
            <div style='{_help_style}'>
                Will wait this many minutes after the last update before publishing.<br />
                Set to 0 to always publish immediately.
            </div>
        """,
        default=5)
    last_updated = models.DateTimeField(
        auto_now=True)
    last_published = models.DateTimeField(
        default=datetime(1970, 1, 1, tzinfo=timezone.utc),
        editable=False)

    @property
    def public_root(self):
        if self.site_root:
            url = self.site_root \
                .replace('https://', '') \
                .replace('http://', '')
            return '/'.join(url.strip('/').split('/')[1:]) + '/'
        else:
            return ''


    def __str__(self):
        return 'Site: ' + self.site


class BaseSiteConfiguration(SingletonModel):
    title = models.CharField(max_length=64)

    class Meta:
        abstract = True

    def __str__(self):
        return self.__class__.__module__.split('.')[0]


class ModelWithSlug(models.Model):
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.__str__())
        super().save(*args, **kwargs)

    class Meta:
        abstract = True