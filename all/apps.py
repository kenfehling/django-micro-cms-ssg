import os
from django.apps import AppConfig
from utils import setup_sites, register_publish_hooks


class AllConfig(AppConfig):
    name = 'all'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            setup_sites()
            register_publish_hooks()
