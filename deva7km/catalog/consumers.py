import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import PreOrder

class PreOrderConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "preorder_updates",
            self.channel_name
        )
        self.send(text_data=json.dumps({
            "message": "WebSocket connection established"
        }))
        print("WebSocket connection established for", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "preorder_updates",
            self.channel_name
        )
        print("WebSocket connection closed for", self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        print(f"Received data: {data}")

    def notify_preorders_update(self, event):
        print(f"notify_preorders_update: {event}")
        self.send(text_data=json.dumps({
            "type": event["type"],
            "event": event["event"],
            "preorder": event["preorder"]
        }))
