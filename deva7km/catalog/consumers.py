import json
import pytz
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from .models import PreOrder


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
        search_text = data.get('search_text')

        if filter_type:
            preorders = await self.filter_preorders(filter_type)
            await self.send_preorders(preorders)
        elif search_text is not None:
            preorders = await self.search_preorders(search_text)
            await self.send_preorders(preorders)

    async def filter_preorders(self, filter_type):
        if filter_type == 'all':
            return await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))
        elif filter_type == 'not-shipped':
            return await sync_to_async(list)(PreOrder.objects.filter(shipped_to_customer=False).order_by('-created_at'))
        elif filter_type == 'not-receipted':
            return await sync_to_async(list)(PreOrder.objects.filter(receipt_issued=False).order_by('-created_at'))
        else:
            return await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))

    async def search_preorders(self, search_text):
        return await sync_to_async(list)(
            PreOrder.objects.filter(
                Q(ttn__icontains=search_text) |
                Q(full_name__icontains=search_text) |
                Q(text__icontains=search_text)
            ).order_by('-created_at')
        )

    async def send_preorders(self, preorders=None):
        if preorders is None:
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))

        preorders_data = await sync_to_async(self.build_preorders_data)(preorders)

        await self.send(text_data=json.dumps({
            'event': 'preorder_list',
            'preorders': preorders_data
        }))

    def build_preorders_data(self, preorders):
        preorders_data = []
        for preorder in preorders:
            last_modified_by_username = preorder.last_modified_by.username if preorder.last_modified_by else 'N/A'
            preorders_data.append({
                'id': preorder.id,
                'full_name': preorder.full_name,
                'text': preorder.text,
                'drop': preorder.drop,
                'created_at': preorder.created_at.isoformat(),  # Используем created_at
                'updated_at': preorder.updated_at.isoformat(),
                'receipt_issued': preorder.receipt_issued,
                'shipped_to_customer': preorder.shipped_to_customer,
                'status': preorder.status,
                'ttn': preorder.ttn,
                'last_modified_by': last_modified_by_username
            })
        return preorders_data
