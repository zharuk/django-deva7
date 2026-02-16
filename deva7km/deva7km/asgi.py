import logging
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import deva7km.routing

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deva7km.settings')

http_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': http_application,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                deva7km.routing.websocket_urlpatterns
            )
        )
    ),
})


if __name__ == "__main__":
    logger.info("Running ASGI application for testing...")
    import uvicorn

    uvicorn.run("deva7km.asgi:application", host="0.0.0.0", port=8000, log_level="debug")
