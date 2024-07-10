import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PreOrder

class PreorderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'preorder_updates',
            self.channel_name
        )
        await self.accept()
        # Отправляем текущие предзаказы при подключении
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
            # Фильтруем предзаказы на основе типа фильтра
            if filter_type == 'all':
                preorders = PreOrder.objects.all()
            elif filter_type == 'not-shipped':
                preorders = PreOrder.objects.filter(shipped_to_customer=False)
            elif filter_type == 'not-receipted':
                preorders = PreOrder.objects.filter(receipt_issued=False)
            else:
                preorders = PreOrder.objects.all()

            await self.send_preorders(preorders)

    async def send_preorders(self, preorders=None):
        if preorders is None:
            preorders = PreOrder.objects.all()

        preorders_data = []
        for preorder in preorders:
            preorders_data.append({
                'id': preorder.id,
                'full_name': preorder.full_name,
                'text': preorder.text,
                'drop': preorder.drop,
                'created_at': preorder.created_at.isoformat(),
                'updated_at': preorder.updated_at.isoformat(),
                'receipt_issued': preorder.receipt_issued,
                'shipped_to_customer': preorder.shipped_to_customer,
                'status': preorder.status,
                'ttn': preorder.ttn
            })

        await self.send(text_data=json.dumps({
            'event': 'preorder_list',
            'preorders': preorders_data
        }))
