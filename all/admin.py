from django.contrib import admin
from all.models import SiteSetup
from utils import publish_site

admin.site.site_header = 'Django Micro CMS/SSG'
admin.site.index_title = 'Admin'
admin.site.site_url = '/'


@admin.register(SiteSetup)
class SiteSettingAdmin(admin.ModelAdmin):
    readonly_fields = ["last_published"]
    actions = ["publish"]

    def publish(self, request, queryset):
        for site_setup in queryset:
            publish_site(site_setup.site)
    publish.short_description = "Publish selected sites"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Sites should be added by adding to the SITES list in config.py
    def has_add_permission(self, request):
        return False
