import inspect
import sys
from django.db.models.signals import post_save
from django.core.management import call_command
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
import subprocess as sub
from more_itertools import flatten
from typing import Any, Callable, Optional, Tuple
from datetime import datetime, timedelta
from config import SITES, BUILD_DIR


def path(s: str,
         route: Callable[[WSGIRequest], HttpResponse],
         distill_func: Optional[Callable] = lambda: None) -> Tuple[Any, Any]:
    from django.urls import path as server_path
    from django_distill import distill_path
    name = route.__name__
    spath = '' if s == '' else s + '/'
    dpath = spath + 'index.html'
    p = server_path(spath, route, name=name)
    dp = distill_path(dpath, route, name=name, distill_func=distill_func)
    return dp, p  # Must be in this order or else url template tags won't work.


def setup_site_group(site: str):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from django.apps import apps
    group, _ = Group.objects.get_or_create(name=site)
    models = apps.all_models[site]

    def get_permissions(model):
        try:
            content_type = ContentType.objects.get(
                app_label=site,
                model=model
            )
            return Permission.objects.filter(content_type=content_type)
        except ContentType.DoesNotExist:
            return []
    permissions = flatten([get_permissions(model) for model in models])
    group.permissions.set(permissions)


def _get_or_create_site_setup(site: str):
    from all.models import SiteSetup
    try:
        return SiteSetup.objects.get(site=site)
    except SiteSetup.DoesNotExist:
        site_setup = SiteSetup(site=site)
        site_setup.save()
        return site_setup


def get_site_setup():
    from all.models import SiteSetup
    frame = inspect.stack()[1]
    module_name = inspect.getmodule(frame[0]).__name__.split('.')[0]
    return SiteSetup.objects.filter(site=module_name).first()


def get_site_cfg():
    frame = inspect.stack()[1]
    module_name = inspect.getmodule(frame[0]).__name__.split('.')[0]
    module = sys.modules.get(f'{module_name}.models')
    SiteConfiguration = module.__dict__['SiteConfiguration']
    try:
        return SiteConfiguration.objects.first()
    except SiteConfiguration.DoesNotExist:
        cfg = SiteConfiguration(site=module_name)
        cfg.save()
        return cfg


def publish_site(site: str):
    """
    site_setup: SiteSetup
    """
    site_setup = _get_or_create_site_setup(site)
    call_command('thumbnail', 'clear_delete_all')
    print('Building site:', site)
    sub.call([
        "bash",
        "scripts/build.sh",
        site,
        site_setup.public_root,
        BUILD_DIR
    ])
    if site_setup.git_repo:
        sub.call([
            "bash",
            "scripts/git.sh",
            site,
            site_setup.git_repo,
            site_setup.public_root,
            BUILD_DIR])
    else:
        print(f'No git repo for site {site} found. Skipping git push.')
    site_setup.last_published = datetime.now()
    site_setup.save()


def update_site(site: str):
    s = _get_or_create_site_setup(site)
    wait_time = timedelta(minutes=s.auto_publish_wait)
    if s.last_updated - s.last_published > wait_time:
        publish_site(site)


def setup_sites():
    for site in SITES:
        _get_or_create_site_setup(site)
        setup_site_group(site)


def register_publish_hooks():
    print('Registering publish hooks')
    def publish(sender, **kwargs):
        for site in SITES:
            if sender._meta.app_label == site:
                update_site(site)

    post_save.connect(publish)
