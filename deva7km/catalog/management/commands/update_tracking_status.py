import asyncio

from django.core.management import BaseCommand

from catalog.novaposhta import update_tracking_status


class Command(BaseCommand):
    help = 'Update tracking statuses from Nova Poshta API'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to update tracking statuses...'))
        asyncio.run(update_tracking_status())
        self.stdout.write(self.style.SUCCESS('Finished updating tracking statuses.'))