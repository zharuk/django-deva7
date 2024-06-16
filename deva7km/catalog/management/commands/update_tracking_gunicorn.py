# deva7km/catalog/management/commands/update_tracking_gunicorn.py
from django.core.management.base import BaseCommand
from catalog.management.commands.update_tracking_status import update_tracking_status


class Command(BaseCommand):
    help = 'Updates tracking statuses using Gunicorn'

    def handle(self, *args, **options):
        update_tracking_status()
        self.stdout.write(self.style.SUCCESS('Successfully updated tracking statuses'))
