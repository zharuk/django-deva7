import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

print("Setting DJANGO_SETTINGS_MODULE...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

print(f"DJANGO_SETTINGS_MODULE={os.getenv('DJANGO_SETTINGS_MODULE')}")

try:
    print("Initializing Django...")
    django.setup()
    print("Django initialized.")
except Exception as e:
    print(f"Error initializing Django: {e}")

try:
    print("Getting ASGI application...")
    application = get_asgi_application()
    print("ASGI application loaded successfully.")
except Exception as e:
    print(f"Error loading ASGI application: {e}")

# Импортируем routing только после полной инициализации Django
try:
    print("Importing routing...")
    import deva7km.routing
    print("Routing imported successfully.")
except Exception as e:
    print(f"Error importing routing: {e}")

try:
    application = ProtocolTypeRouter({
        'http': application,
        'websocket': AuthMiddlewareStack(
            URLRouter(
                deva7km.routing.websocket_urlpatterns
            )
        ),
    })
    print("ASGI setup completed.")
except Exception as e:
    print(f"Error setting up ASGI: {e}")

# Для теста запустите этот файл отдельно
if __name__ == "__main__":
    print("Running ASGI application for testing...")
    import uvicorn
    uvicorn.run("deva7km.asgi:application", host="0.0.0.0", port=8000, log_level="debug")
