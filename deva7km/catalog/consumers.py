import json
import logging
import requests
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import translation, timezone
from .models import PreOrder
from .novaposhta import get_tracking_status, update_tracking_status

class PreorderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('preorder_updates', self.channel_name)
        await self.accept()
        self.active_filter = 'all'
        await self.send_preorders()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('preorder_updates', self.channel_name)

    async def notify_preorders_update(self, event):
        preorder = event['preorder']
        matches_filter = await self.matches_active_filter(preorder)

        if matches_filter:
            preorder_html = await sync_to_async(render_to_string)('seller_cabinet/preorders/preorder_card.html',
                                                                  {'preorders': [preorder]})
            await self.send(text_data=json.dumps({
                'event': event['event'],
                'html': preorder_html,
                'preorder_id': preorder['id']
            }))
        else:
            await self.send(text_data=json.dumps({
                'event': 'preorder_deleted',
                'preorder_id': preorder['id']
            }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        filter_type = data.get('filter')
        search_text = data.get('search_text')
        switch_type = data.get('type')
        id = data.get('id')
        status = data.get('status')
        ttns = data.get('ttns')

        if filter_type:
            self.active_filter = filter_type
            preorders = await self.filter_preorders(filter_type)
            await self.send_preorders(preorders)
        elif search_text is not None:
            preorders = await self.search_preorders(search_text)
            await self.send_preorders(preorders)
        elif switch_type and id is not None and status is not None:
            await self.update_switch_status(switch_type, id, status)
        elif ttns:
            logging.info(f"Обновление статусов для TTNs: {ttns}")
            await update_tracking_status()

    async def filter_preorders(self, filter_type):
        if filter_type == 'all':
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))
        elif filter_type == 'not-shipped':
            preorders = await sync_to_async(list)(
                PreOrder.objects.filter(shipped_to_customer=False).order_by('-created_at'))
        elif filter_type == 'not-receipted':
            preorders = await sync_to_async(list)(PreOrder.objects.filter(receipt_issued=False).order_by('-created_at'))
        elif filter_type == 'not-paid':
            preorders = await sync_to_async(list)(
                PreOrder.objects.filter(payment_received=False).order_by('-created_at'))
        else:
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))

        return preorders

    async def search_preorders(self, search_text):
        preorders = await sync_to_async(list)(
            PreOrder.objects.filter(
                Q(ttn__icontains=search_text) |
                Q(full_name__icontains=search_text) |
                Q(text__icontains=search_text)
            ).order_by('-created_at')
        )
        return preorders

    async def update_switch_status(self, switch_type, id, status):
        preorder = await sync_to_async(PreOrder.objects.get)(id=id)

        if switch_type == 'toggle_receipt':
            preorder.receipt_issued = status
        elif switch_type == 'toggle_shipped':
            preorder.shipped_to_customer = status
        elif switch_type == 'toggle_payment':
            preorder.payment_received = status

        await sync_to_async(preorder.save)()
        await self.notify_preorders_update({
            'event': 'preorder_updated',
            'preorder': self.build_preorder_data(preorder)
        })

    async def send_preorders(self, preorders=None):
        if preorders is None:
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))

        preorders_data = await sync_to_async(self.build_preorders_data)(preorders)
        html = await sync_to_async(render_to_string)('seller_cabinet/preorders/preorder_card.html',
                                                     {'preorders': preorders_data})

        await self.send(text_data=json.dumps({
            'event': 'preorder_list',
            'html': html
        }))

    def build_preorders_data(self, preorders):
        preorders_data = []
        for preorder in preorders:
            preorders_data.append(self.build_preorder_data(preorder))
        return preorders_data

    def build_preorder_data(self, preorder):
        last_modified_by = preorder.last_modified_by.username if preorder.last_modified_by else 'N/A'

        with translation.override('ru'):
            created_at_local = timezone.localtime(preorder.created_at)
            updated_at_local = timezone.localtime(preorder.updated_at)

        return {
            'id': preorder.id,
            'full_name': preorder.full_name,
            'text': preorder.text,
            'drop': preorder.drop,
            'created_at': created_at_local,
            'updated_at': updated_at_local,
            'receipt_issued': preorder.receipt_issued,
            'shipped_to_customer': preorder.shipped_to_customer,
            'payment_received': preorder.payment_received,
            'status': preorder.status,
            'ttn': preorder.ttn,
            'last_modified_by': last_modified_by,
        }

    async def matches_active_filter(self, preorder):
        if self.active_filter == 'all':
            return True
        if self.active_filter == 'not-shipped' and preorder['shipped_to_customer']:
            return False
        if self.active_filter == 'not-receipted' and preorder['receipt_issued']:
            return False
        if self.active_filter == 'not-paid' and preorder['payment_received']:
            return False
        return True
