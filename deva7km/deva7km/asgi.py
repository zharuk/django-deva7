import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import deva7km.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            deva7km.routing.websocket_urlpatterns
        )
    ),
})

# Для теста запустите этот файл отдельно
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("deva7km.asgi:application", host="0.0.0.0", port=8000, log_level="info")
