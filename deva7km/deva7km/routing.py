from django.urls import path
from catalog.consumers import PreorderConsumer

websocket_urlpatterns = [
    path('ws/preorders/', PreorderConsumer.as_asgi()),
]
