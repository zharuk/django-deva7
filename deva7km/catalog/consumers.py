import json
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.db.models import Q
from .models import PreOrder, ProductModification, Sale, SaleItem, TelegramUser
from .novaposhta import update_tracking_status


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
        counts = await self.get_preorder_counts()

        if matches_filter:
            preorder_html = await sync_to_async(render_to_string)('seller_cabinet/preorders/preorder_card.html',
                                                                  {'preorders': [preorder]})
            await self.send(text_data=json.dumps({
                'event': event['event'],
                'html': preorder_html,
                'preorder_id': preorder['id'],
                'counts': counts
            }))
        else:
            await self.send(text_data=json.dumps({
                'event': 'preorder_deleted',
                'preorder_id': preorder['id'],
                'counts': counts
            }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        filter_type = data.get('filter')
        search_text = data.get('search_text')
        switch_type = data.get('type')
        id = data.get('id')
        status = data.get('status')
        ttns = data.get('ttns')
        user_id = data.get('user_id')  # Получаем user_id из данных

        if filter_type:
            self.active_filter = filter_type
            preorders = await self.filter_preorders(filter_type)
            await self.send_preorders(preorders)
        elif search_text is not None:
            preorders = await self.search_preorders(search_text)
            await self.send_preorders(preorders)
        elif switch_type and id is not None and status is not None:
            await self.update_switch_status(switch_type, id, status, user_id)  # Передаем user_id
        elif ttns:
            logging.info(f"Обновление статусов для TTNs: {ttns}")
            await update_tracking_status()
            await self.send(text_data=json.dumps({
                'event': 'update_complete',
                'message': 'Все TTN были успешно обновлены.'
            }))

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

    async def update_switch_status(self, switch_type, id, status, user_id):
        preorder = await sync_to_async(PreOrder.objects.get)(id=id)
        user = await sync_to_async(User.objects.get)(id=user_id)

        if switch_type == 'toggle_receipt':
            preorder.receipt_issued = status
        elif switch_type == 'toggle_shipped':
            preorder.shipped_to_customer = status
        elif switch_type == 'toggle_payment':
            preorder.payment_received = status

        preorder.last_modified_by = user
        await sync_to_async(preorder.save)()
        await self.notify_preorders_update({
            'event': 'preorder_updated',
            'preorder': self.build_preorder_data(preorder)
        })

    async def send_preorders(self, preorders=None):
        if preorders is None:
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))

        preorders_data = await sync_to_async(self.build_preorders_data)(preorders)
        counts = await self.get_preorder_counts()
        html = await sync_to_async(render_to_string)('seller_cabinet/preorders/preorder_card.html',
                                                     {'preorders': preorders_data})

        await self.send(text_data=json.dumps({
            'event': 'preorder_list',
            'html': html,
            'counts': counts
        }))

    async def get_preorder_counts(self):
        counts = {
            'all': await sync_to_async(PreOrder.objects.count)(),
            'not_shipped': await sync_to_async(PreOrder.objects.filter(shipped_to_customer=False).count)(),
            'not_receipted': await sync_to_async(PreOrder.objects.filter(receipt_issued=False).count)(),
            'not_paid': await sync_to_async(PreOrder.objects.filter(payment_received=False).count)(),
        }
        return counts

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


class SalesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        print("Полученные данные: ", data)  # Отладочная информация
        data_type = data.get('type')
        if data_type == 'search':
            self.search_items(data.get('query', ''))
        elif data_type == 'add_item':
            self.add_item_to_sale(data.get('custom_sku', ''), data.get('quantity', 1))
        elif data_type == 'create_sale':
            self.create_sale(data.get('user_id'), data.get('telegram_user_id'), data.get('source'), data.get('payment_method'), data.get('comment', ''), data.get('items'))
        elif data_type == 'update_total':
            self.update_total(data.get('total', 0))
        elif data_type == 'item_added':
            self.item_added(data.get('custom_sku', ''))

    def search_items(self, query):
        results = ProductModification.objects.filter(custom_sku__icontains=query)
        products = [{'name': f"{r.product.title}-{r.custom_sku}", 'stock': r.stock, 'price': r.product.price, 'custom_sku': r.custom_sku} for r in results]
        self.send(text_data=json.dumps({
            'type': 'search_results',
            'results': products
        }))

    def add_item_to_sale(self, custom_sku, quantity):
        try:
            product_modification = ProductModification.objects.get(custom_sku=custom_sku)
            if product_modification.stock < quantity:
                self.send(text_data=json.dumps({
                    'type': 'item_not_available',
                    'custom_sku': custom_sku
                }))
            else:
                sale_item = SaleItem.objects.create(
                    sale=self.get_current_sale(),
                    product_modification=product_modification,
                    quantity=quantity
                )
                product_modification.stock -= quantity
                product_modification.save()
                self.send(text_data=json.dumps({
                    'type': 'item_added',
                    'custom_sku': custom_sku,
                    'quantity': quantity,
                    'price': sale_item.total_price()
                }))
        except ObjectDoesNotExist:
            self.send(text_data=json.dumps({
                'type': 'item_not_available',
                'custom_sku': custom_sku
            }))

    def create_sale(self, user_id, telegram_user_id, source, payment_method, comment, items):
        sale = Sale.objects.create(
            user_id=user_id,
            telegram_user_id=telegram_user_id,
            source=source,
            payment_method=payment_method,
            comment=comment
        )

        for item in items:
            product_modification = ProductModification.objects.get(custom_sku=item['custom_sku'])
            SaleItem.objects.create(
                sale=sale,
                product_modification=product_modification,
                quantity=item['quantity']
            )

        sale.total_amount = sum(item['quantity'] * item['price'] for item in items)
        sale.save()

        # Отправка подтверждения продажи
        self.send(text_data=json.dumps({
            'type': 'sell_confirmation',
            'status': 'success',
            'sale_id': sale.id
        }))

    def get_current_sale(self):
        return Sale.objects.get_or_create(status='pending')[0]

    def update_total(self, total):
        self.send(text_data=json.dumps({
            'type': 'update_total',
            'total': total
        }))

    def item_added(self, custom_sku):
        try:
            product_modification = ProductModification.objects.get(custom_sku=custom_sku)
            if product_modification.stock < 1:
                self.send(text_data=json.dumps({
                    'type': 'item_not_available',
                    'custom_sku': custom_sku
                }))
            else:
                self.send(text_data=json.dumps({
                    'type': 'item_added',
                    'custom_sku': custom_sku
                }))
        except ObjectDoesNotExist:
            self.send(text_data=json.dumps({
                'type': 'sell_error',
                'message': f'ProductModification with custom_sku {custom_sku} does not exist.'
            }))
