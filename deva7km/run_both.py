import os
import django
import threading
import time


def setup_django_environment():
    # Установка переменной окружения DJANGO_SETTINGS_MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

    # Инициализация Django
    django.setup()


def run_update_tracking():
    # Поместим импорт здесь, чтобы убедиться, что Django настроен
    from catalog.management.commands import update_tracking_status
    update_tracking_status.update_tracking_status()


def run_server():
    # Запускаем сервер Django
    os.system("python manage.py runserver")


if __name__ == "__main__":
    try:
        # Настройка окружения Django
        setup_django_environment()

        # Создаем и запускаем поток для сервера
        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        # Ждем некоторое время, чтобы сервер успел запуститься
        time.sleep(10)  # Увеличьте это значение при необходимости

        # Запускаем обновление статусов треков после запуска сервера
        run_update_tracking()

        # Дожидаемся завершения потока сервера
        server_thread.join()

    except KeyboardInterrupt:
        # Обработка прерывания пользователем
        print("run_both.py: Скрипт был прерван пользователем")
