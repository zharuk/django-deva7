# deva7km/routing.py

from django.urls import path
from catalog import consumers
from catalog.consumers import PreOrderConsumer

websocket_urlpatterns = [
    path('ws/preorders/', PreOrderConsumer.as_asgi()),
]
