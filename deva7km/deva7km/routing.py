from django.urls import path

from catalog.consumers import PreorderConsumer, SalesConsumer, ReturnConsumer, InventoryConsumer, WriteOffConsumer

websocket_urlpatterns = [
    path('ws/preorders/', PreorderConsumer.as_asgi()),
    path('ws/sales/', SalesConsumer.as_asgi()),
    path('ws/returns/', ReturnConsumer.as_asgi()),
    path('ws/inventory/', InventoryConsumer.as_asgi()),
    path("ws/write_off/", WriteOffConsumer.as_asgi()),
]
