import os


# Функция для запуска runbot
def run_bot():
    os.system("python manage.py runbot")


if __name__ == "__main__":
    try:
        # Запуск runbot в основном потоке
        run_bot()
    except KeyboardInterrupt:
        # При прерывании скрипта пользователем выполните необходимые действия
        print("run_both.py: Скрипт был прерван пользователем")
