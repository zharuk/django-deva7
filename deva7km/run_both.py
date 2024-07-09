import os
import django
import threading
import time
import uvicorn


def setup_django_environment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')
    django.setup()
    print("Django environment set up.")


def run_server():
    print("Starting Uvicorn server...")
    uvicorn.run("deva7km.asgi:application", host="0.0.0.0", port=8000, log_level="info")


def run_bot():
    print("Starting bot...")
    os.system("python run_bot.py")


if __name__ == "__main__":
    try:
        setup_django_environment()

        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()

        server_thread.join()
        bot_thread.join()

    except KeyboardInterrupt:
        print("run_both.py: Скрипт был прерван пользователем")
