import os
import django
import threading
import time


def setup_django_environment():
    # Установка переменной окружения DJANGO_SETTINGS_MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

    # Инициализация Django
    django.setup()


def run_server():
    # Запускаем сервер Uvicorn
    os.system("uvicorn deva7km.asgi:application --host 0.0.0.0 --port 8000")


def run_bot():
    # Пример запуска вашего бота (замените на фактический запуск вашего бота)
    os.system("python run_bot.py")


if __name__ == "__main__":
    try:
        # Настройка окружения Django
        setup_django_environment()

        # Создаем и запускаем поток для сервера
        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        # Создаем и запускаем поток для бота
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()

        # Ждем некоторое время, чтобы сервер успел запуститься
        time.sleep(10)  # Увеличьте это значение при необходимости

        # Дожидаемся завершения потоков сервера и бота
        server_thread.join()
        bot_thread.join()

    except KeyboardInterrupt:
        # Обработка прерывания пользователем
        print("run_both.py: Скрипт был прерван пользователем")
