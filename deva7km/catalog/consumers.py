import json
import logging
from datetime import datetime

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.db.models import Q
from .models import PreOrder, ProductModification, Sale, SaleItem, TelegramUser, Return, ReturnItem, Inventory, \
    InventoryItem, WriteOff, WriteOffItem
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


class SalesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        data_type = data.get('type')
        if data_type == 'search':
            await self.search_items(data.get('query', ''))
        elif data_type == 'add_item':
            await self.add_item_to_sale(data.get('custom_sku', ''), data.get('quantity', 1))
        elif data_type == 'create_sale':
            await self.create_sale(
                data.get('user_id'),
                data.get('telegram_user_id'),
                data.get('source'),
                data.get('payment_method'),
                data.get('comment', ''),
                data.get('items')
            )
        elif data_type == 'update_total':
            await self.update_total(data.get('total', 0))
        elif data_type == 'item_added':
            await self.item_added(data.get('custom_sku', ''))
        elif data_type == 'get_sales_list':
            await self.send_sales_list()

    async def search_items(self, query):
        results = await sync_to_async(list)(
            ProductModification.objects.filter(custom_sku__icontains=query)
        )
        products = [{
            'name': f"{r.product.title}-{r.custom_sku}",
            'stock': r.stock,
            'price': r.product.price,
            'custom_sku': r.custom_sku,
            'thumbnail': r.thumbnail_image_url()
        } for r in results]
        await self.send(text_data=json.dumps({
            'type': 'search_results',
            'results': products
        }))

    async def add_item_to_sale(self, custom_sku, quantity):
        try:
            product_modification = await sync_to_async(ProductModification.objects.get)(custom_sku=custom_sku)
            if product_modification.stock < quantity:
                await self.send(text_data=json.dumps({
                    'type': 'item_not_available',
                    'custom_sku': custom_sku
                }))
            else:
                sale_item = await sync_to_async(SaleItem.objects.create)(
                    sale=await self.get_current_sale(),
                    product_modification=product_modification,
                    quantity=quantity
                )
                product_modification.stock -= quantity
                await sync_to_async(product_modification.save)()
                await self.send(text_data=json.dumps({
                    'type': 'item_added',
                    'custom_sku': custom_sku,
                    'quantity': quantity,
                    'price': sale_item.total_price()
                }))
        except ObjectDoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'item_not_available',
                'custom_sku': custom_sku
            }))

    async def create_sale(self, user_id, telegram_user_id, source, payment_method, comment, items):
        sale = await sync_to_async(Sale.objects.create)(
            user_id=user_id,
            telegram_user_id=telegram_user_id,
            source=source,
            payment_method=payment_method,
            comment=comment
        )

        for item in items:
            product_modification = await sync_to_async(ProductModification.objects.get)(custom_sku=item['custom_sku'])
            await sync_to_async(SaleItem.objects.create)(
                sale=sale,
                product_modification=product_modification,
                quantity=item['quantity']
            )

        sale.total_amount = sum(item['quantity'] * item['price'] for item in items)
        await sync_to_async(sale.save)()

        await self.send(text_data=json.dumps({
            'type': 'sell_confirmation',
            'status': 'success',
            'sale_id': sale.id
        }))

    async def send_sales_list(self):
        today = timezone.localtime(timezone.now()).date()  # Используем локальную дату
        sales = await sync_to_async(list)(
            Sale.objects.filter(created_at__date=today).order_by('-created_at')  # Сортируем от самых новых
        )
        sales_data = []
        for sale in sales:
            items_data = []
            for item in await sync_to_async(list)(sale.items.all()):
                product_modification = await sync_to_async(lambda: item.product_modification)()
                custom_sku = await sync_to_async(lambda: product_modification.custom_sku)()
                total_price = await sync_to_async(item.total_price)()
                thumbnail = await sync_to_async(lambda: product_modification.thumbnail_image_url())()
                items_data.append({
                    'custom_sku': custom_sku,
                    'quantity': item.quantity,
                    'total_price': total_price,
                    'thumbnail': thumbnail
                })
            sales_data.append({
                'id': sale.id,
                'created_at': timezone.localtime(sale.created_at).strftime('%Y-%m-%d %H:%M:%S'),  # Преобразуем время в локальное
                'user': await sync_to_async(lambda: sale.user.username if sale.user else 'Неизвестно')(),
                'items': items_data,
                'total_amount': await sync_to_async(sale.calculate_total_amount)(),
                'payment_method': sale.get_payment_method_display(),
                'comment': sale.comment
            })
        await self.send(text_data=json.dumps({
            'type': 'sales_list',
            'sales': sales_data
        }))

    async def get_current_sale(self):
        sale, _ = await sync_to_async(Sale.objects.get_or_create)(status='pending')
        return sale

    async def update_total(self, total):
        await self.send(text_data=json.dumps({
            'type': 'update_total',
            'total': total
        }))

    async def item_added(self, custom_sku):
        try:
            product_modification = await sync_to_async(ProductModification.objects.get)(custom_sku=custom_sku)
            if product_modification.stock < 1:
                await self.send(text_data=json.dumps({
                    'type': 'item_not_available',
                    'custom_sku': custom_sku
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'item_added',
                    'custom_sku': custom_sku
                }))
        except ObjectDoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'sell_error',
                'message': f'ProductModification with custom_sku {custom_sku} does not exist.'
            }))


class ReturnConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'create_return':
            await self.create_return(data)
        elif data['type'] == 'get_returns_list':
            await self.send_return_list()

    async def create_return(self, data):
        items = data['items']

        try:
            user = await sync_to_async(User.objects.get)(id=data['user_id'])
        except User.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'return_error',
                'message': 'User not found'
            }))
            return

        try:
            return_obj = Return(
                user=user,
                comment=data['comment']
            )
            await sync_to_async(return_obj.save)()

            for item in items:
                product_modification = await sync_to_async(ProductModification.objects.get)(
                    custom_sku=item['custom_sku'])
                return_item = ReturnItem(
                    return_sale=return_obj,  # Используем правильное поле
                    product_modification=product_modification,
                    quantity=item['quantity']
                )
                await sync_to_async(return_item.save)()

            await self.send(text_data=json.dumps({
                'type': 'return_confirmation',
                'status': 'success'
            }))

            await self.send_return_list()
        except ProductModification.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'return_error',
                'message': f'Product modification with SKU {item["custom_sku"]} not found'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'return_error',
                'message': str(e)
            }))

    async def send_return_list(self):
        today = timezone.localtime(timezone.now()).date()
        returns = await sync_to_async(list)(
            Return.objects.filter(created_at__date=today).order_by('-created_at')
        )
        returns_data = [await self.return_to_dict(return_obj) for return_obj in returns]
        await self.send(text_data=json.dumps({
            'type': 'returns_list',
            'returns': returns_data
        }))

    async def return_to_dict(self, return_obj):
        user = await sync_to_async(lambda: return_obj.user.username if return_obj.user else 'Неизвестно')()
        items = await sync_to_async(list)(return_obj.items.all())
        items_data = []

        for item in items:
            product_modification = await sync_to_async(lambda: item.product_modification)()
            custom_sku = await sync_to_async(lambda: product_modification.custom_sku)()
            quantity = item.quantity
            total_price = await sync_to_async(item.total_price)()
            thumbnail = await sync_to_async(product_modification.thumbnail_image_url)()
            items_data.append({
                'custom_sku': custom_sku,
                'quantity': quantity,
                'total_price': total_price,
                'thumbnail': thumbnail,
            })

        return {
            'id': return_obj.id,
            'created_at': return_obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user': user,
            'total_amount': await sync_to_async(return_obj.calculate_total_amount)(),
            'items': items_data,
            'comment': return_obj.comment
        }


class InventoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'create_inventory':
            await self.create_inventory(data)
        elif data['type'] == 'get_inventory_list':
            await self.send_inventory_list()

    async def create_inventory(self, data):
        items = data['items']

        try:
            user = await sync_to_async(User.objects.get)(id=data['user_id'])
        except User.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'inventory_error',
                'message': 'User not found'
            }))
            return

        try:
            inventory_obj = Inventory(
                user=user,
                comment=data['comment']
            )
            await sync_to_async(inventory_obj.save)()

            for item in items:
                product_modification = await sync_to_async(ProductModification.objects.get)(
                    custom_sku=item['custom_sku'])
                inventory_item = InventoryItem(
                    inventory=inventory_obj,
                    product_modification=product_modification,
                    quantity=item['quantity']
                )
                await sync_to_async(inventory_item.save)()

            await self.send(text_data=json.dumps({
                'type': 'inventory_confirmation',
                'status': 'success'
            }))

            await self.send_inventory_list()
        except ProductModification.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'inventory_error',
                'message': f'Product modification with SKU {item["custom_sku"]} not found'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'inventory_error',
                'message': str(e)
            }))

    async def send_inventory_list(self):
        today = timezone.localtime(timezone.now()).date()
        inventories = await sync_to_async(list)(
            Inventory.objects.filter(created_at__date=today).order_by('-created_at')
        )
        inventories_data = [await self.inventory_to_dict(inventory) for inventory in inventories]
        await self.send(text_data=json.dumps({
            'type': 'inventories_list',
            'inventories': inventories_data
        }))

    async def inventory_to_dict(self, inventory_obj):
        user = await sync_to_async(lambda: inventory_obj.user.username if inventory_obj.user else 'Неизвестно')()
        items = await sync_to_async(list)(inventory_obj.items.all())
        items_data = []

        for item in items:
            product_modification = await sync_to_async(lambda: item.product_modification)()
            custom_sku = await sync_to_async(lambda: product_modification.custom_sku)()
            quantity = item.quantity
            total_price = await sync_to_async(item.total_price)()
            thumbnail = await sync_to_async(product_modification.thumbnail_image_url)()
            items_data.append({
                'custom_sku': custom_sku,
                'quantity': quantity,
                'total_price': total_price,
                'thumbnail': thumbnail,
            })

        return {
            'id': inventory_obj.id,
            'created_at': inventory_obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user': user,
            'total_amount': await sync_to_async(inventory_obj.calculate_total_amount)(),
            'items': items_data
        }


class WriteOffConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'create_write_off':
            await self.create_write_off(data)
        elif data['type'] == 'get_write_off_list':
            await self.send_write_off_list()

    async def create_write_off(self, data):
        items = data['items']

        try:
            user = await sync_to_async(User.objects.get, thread_sensitive=True)(id=data['user_id'])
        except User.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'write_off_error',
                'message': 'User not found'
            }))
            return

        try:
            # Используем sync_to_async с thread_sensitive=True для создания записи
            write_off = await sync_to_async(WriteOff.objects.create, thread_sensitive=True)(
                user=user,
                telegram_user_id=data.get('telegram_user_id'),
                source=data['source'],
                comment=data['comment']
            )

            for item in items:
                product_modification = await sync_to_async(ProductModification.objects.get, thread_sensitive=True)(
                    custom_sku=item['custom_sku'])
                await sync_to_async(WriteOffItem.objects.create, thread_sensitive=True)(
                    write_off=write_off,
                    product_modification=product_modification,
                    quantity=item['quantity']
                )

            await self.send(text_data=json.dumps({
                'type': 'write_off_confirmation',
                'status': 'success'
            }))

            await self.send_write_off_list()
        except ProductModification.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'write_off_error',
                'message': f'Product modification with SKU {item["custom_sku"]} not found'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'write_off_error',
                'message': str(e)
            }))

    async def send_write_off_list(self):
        today = timezone.localtime(timezone.now()).date()
        write_offs = await sync_to_async(list)(
            WriteOff.objects.filter(created_at__date=today).order_by('-created_at')
        )
        await self.send(text_data=json.dumps({
            'type': 'write_offs_list',
            'write_offs': [await self.write_off_to_dict(write_off) for write_off in write_offs]
        }))

    async def write_off_to_dict(self, write_off):
        user_username = await sync_to_async(lambda: write_off.user.username if write_off.user else 'Неизвестно')()
        total_amount = await sync_to_async(write_off.calculate_total_amount)()
        items = await sync_to_async(list)(write_off.items.all())

        # Получение данных о каждом элементе в асинхронном режиме
        items_data = []
        for item in items:
            product_modification = await sync_to_async(lambda: item.product_modification)()
            thumbnail_url = await sync_to_async(product_modification.thumbnail_image_url)()
            items_data.append({
                'custom_sku': product_modification.custom_sku,
                'quantity': item.quantity,
                'total_price': await sync_to_async(item.total_price)(),
                'thumbnail': thumbnail_url
            })

        return {
            'id': write_off.id,
            'created_at': write_off.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user': user_username,
            'total_amount': total_amount,
            'items': items_data,
        }
