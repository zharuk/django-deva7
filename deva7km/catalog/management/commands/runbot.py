import asyncio
from django.core.management.base import BaseCommand
from bot.bot import main  # Подключите функцию main из вашего бота


class Command(BaseCommand):
    help = 'Запустить бот'

    def handle(self, *args, **options):
        asyncio.run(main())
