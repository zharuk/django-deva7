import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PreOrder
from datetime import datetime

class PreorderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'preorder_updates',
            self.channel_name
        )
        await self.accept()
        await self.send_preorders()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'preorder_updates',
            self.channel_name
        )

    async def notify_preorders_update(self, event):
        preorder = event['preorder']
        await self.send(text_data=json.dumps({
            'event': event['event'],
            'preorder': preorder
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        filter_type = data.get('filter')

        if filter_type:
            preorders = await self.filter_preorders(filter_type)
            await self.send_preorders(preorders)

    async def filter_preorders(self, filter_type):
        if filter_type == 'all':
            return await sync_to_async(list)(PreOrder.objects.all())
        elif filter_type == 'not-shipped':
            return await sync_to_async(list)(PreOrder.objects.filter(shipped_to_customer=False))
        elif filter_type == 'not-receipted':
            return await sync_to_async(list)(PreOrder.objects.filter(receipt_issued=False))
        else:
            return await sync_to_async(list)(PreOrder.objects.all())

    async def send_preorders(self, preorders=None):
        if preorders is None:
            preorders = await sync_to_async(list)(PreOrder.objects.all())

        preorders_data = [{
            'id': preorder.id,
            'full_name': preorder.full_name,
            'text': preorder.text,
            'drop': preorder.drop,
            'created_at': preorder.created_at.strftime('%d.%m.%Y %H:%M:%S'),
            'updated_at': preorder.updated_at.strftime('%d.%m.%Y %H:%M:%S'),
            'receipt_issued': preorder.receipt_issued,
            'shipped_to_customer': preorder.shipped_to_customer,
            'status': preorder.status,
            'ttn': preorder.ttn
        } for preorder in preorders]

        await self.send(text_data=json.dumps({
            'event': 'preorder_list',
            'preorders': preorders_data
        }))