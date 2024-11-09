import os

# Укажите путь к вашим настройкам
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django

# Инициализируем настройки Django
django.setup()

def check_redis_connection():
    channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer.send)("test_channel", {"type": "test.message", "text": "hello"})
        message = async_to_sync(channel_layer.receive)("test_channel")
        if message["text"] == "hello":
            print("Redis подключен и работает корректно.")
        else:
            print("Ошибка: сообщение не совпадает с отправленным.")
    except Exception as e:
        print("Ошибка подключения к Redis:", e)

check_redis_connection()
