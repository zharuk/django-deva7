import os
import threading
import logging

# Настройка логирования в тот же файл, что и у бота
logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')


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
        print("Скрипт был прерван пользователем")
