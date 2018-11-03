"""
Restart celery on django dev server restart
"""
import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    """
    Kill celery process and start it againg
    """
    cmd = 'pkill ../venv/bin/celery'
    subprocess.call(shlex.split(cmd))
    cmd = '../venv/bin/celery -A music_decompose worker -l info'
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):
    """
    Django management command
    """

    def handle(self, *args, **options):
        """
        Restart celery on django dev server restart
        """
        print('Starting celery worker with autoreload...')
        autoreload.main(restart_celery)
