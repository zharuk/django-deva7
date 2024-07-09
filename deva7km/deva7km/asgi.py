import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import deva7km.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            deva7km.routing.websocket_urlpatterns
        )
    ),
})
