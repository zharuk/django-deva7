import os
import threading


# Функция для запуска runserver
def run_server():
    os.system("python manage.py runserver")


# Функция для запуска runbot
def run_bot():
    os.system("python manage.py runbot")


if __name__ == "__main__":
    try:

        # Создание и запуск потока для runserver
        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        # Запуск runbot в основном потоке
        run_bot()

        # Дождитесь завершения потока runserver
        server_thread.join()
    except KeyboardInterrupt:
        # При прерывании скрипта пользователем выполните необходимые действия
        print("run_both.py: Скрипт был прерван пользователем")
