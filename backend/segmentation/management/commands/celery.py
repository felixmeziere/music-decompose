import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = 'pkill ../venv/bin/celery'
    subprocess.call(shlex.split(cmd))
    cmd = '../venv/bin/celery -A music_decompose worker -l info'
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.main(restart_celery)
