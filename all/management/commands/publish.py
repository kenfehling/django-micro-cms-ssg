from django.conf import settings
from django.core.management.base import BaseCommand
from utils import publish_site


def _main(site: str):
    publish_site(site)


class Command(BaseCommand):
    help = 'Builds and publishes a static site to a git repo'

    def add_arguments(self, parser):
        parser.add_argument('--site', default='', dest='site', help='The site to build')

    def handle(self, *args, **kwargs):
        site = kwargs['site']

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        _main(site)
