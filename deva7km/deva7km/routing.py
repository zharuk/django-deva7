from django.urls import path

from catalog.consumers import PreorderConsumer, SalesConsumer

websocket_urlpatterns = [
    path('ws/preorders/', PreorderConsumer.as_asgi()),
    path('ws/sales/', SalesConsumer.as_asgi()),
]
