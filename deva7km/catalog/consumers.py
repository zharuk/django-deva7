import json
import re
from datetime import timedelta, datetime

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.db.models import Q

from .forms import PreOrderForm
from .models import PreOrder, ProductModification, Sale, SaleItem, Return, ReturnItem, Inventory, \
    InventoryItem, WriteOff, WriteOffItem, TelegramUser, Product
from .novaposhta import update_tracking_status


class PreorderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('preorder_updates', self.channel_name)
        await self.accept()
        self.active_filter = 'all'
        await self.send_preorders_update()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('preorder_updates', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        if event_type == 'filter':
            self.active_filter = data.get('filter', 'all')
            await self.send_preorders_update()
        elif event_type == 'search':
            await self.handle_search(data)
        elif event_type == 'get_preorder':
            await self.handle_get_preorder(data)
        elif event_type in ['toggle_receipt', 'toggle_shipped', 'toggle_payment']:
            await self.handle_toggle_status(event_type, data)
        elif event_type == 'create_or_edit':
            await self.handle_create_or_edit(data)
        elif event_type == 'delete':
            await self.handle_delete(data)
        elif event_type == 'update_ttns':
            await self.handle_ttn_update()
        elif event_type == 'notify_preorders_update':
            await self.notify_preorders_update(data)

    async def notify_preorders_update(self, event):
        event_type = event.get('event')
        preorder_id = event.get('preorder_id')

        # Вызываем метод обновления предзаказов, чтобы отправить актуальные данные клиентам
        await self.send_preorders_update()

        # Если нужно, можно передать дополнительную информацию клиенту
        await self.send(text_data=json.dumps({
            'event': event_type,
            'preorder_id': preorder_id,
        }))

    async def handle_get_preorder(self, data):
        preorder_id = data.get('id')
        preorder = await sync_to_async(PreOrder.objects.get)(pk=preorder_id)
        form_data = {
            'preorder_id': preorder.id,
            'full_name': preorder.full_name,
            'text': preorder.text,
            'drop': preorder.drop,
            'receipt_issued': preorder.receipt_issued,
            'ttn': preorder.ttn,
            'shipped_to_customer': preorder.shipped_to_customer,
            'status': preorder.status,
            'payment_received': preorder.payment_received,
        }
        await self.send(text_data=json.dumps({
            'event': 'get_preorder',
            **form_data
        }))

    async def handle_search(self, data):
        search_text = data.get('search_text', '')
        preorders = await self.search_preorders(search_text)
        await self.send_preorders_update(preorders=preorders)

    async def handle_toggle_status(self, switch_type, data):
        preorder_id = data.get('id')
        status = data.get('status')
        user_id = data.get('user_id')
        preorder = await sync_to_async(PreOrder.objects.get)(pk=preorder_id)
        user = await sync_to_async(User.objects.get)(pk=user_id)

        if switch_type == 'toggle_receipt':
            preorder.receipt_issued = status
        elif switch_type == 'toggle_shipped':
            preorder.shipped_to_customer = status
        elif switch_type == 'toggle_payment':
            preorder.payment_received = status

        preorder.last_modified_by = user
        await sync_to_async(preorder.save)()
        await self.send_preorders_update()

    async def handle_create_or_edit(self, data):
        preorder_id = data.get('id')
        preorder = await sync_to_async(PreOrder.objects.get)(pk=preorder_id) if preorder_id else PreOrder()

        form_data = data.get('form_data')
        form = PreOrderForm(form_data, instance=preorder)
        if form.is_valid():
            preorder = form.save(commit=False)
            user = await sync_to_async(User.objects.get)(id=data.get('user_id'))
            preorder.last_modified_by = user
            await sync_to_async(preorder.save)()

            # Вместо отправки отдельного события 'preorder_saved',
            # мы передаем дополнительное событие в send_preorders_update
            await self.send_preorders_update(additional_event='preorder_saved')
        else:
            await self.send(text_data=json.dumps({
                'event': 'form_invalid',
                'errors': form.errors,
            }))

    async def handle_delete(self, data):
        preorder_id = data.get('id')
        preorder = await sync_to_async(PreOrder.objects.get)(pk=preorder_id)
        await sync_to_async(preorder.delete)()
        await self.send_preorders_update()

    async def handle_ttn_update(self):
        await update_tracking_status()
        await self.send_preorders_update()
        await self.send(text_data=json.dumps({
            'event': 'update_complete',
            'message': 'Все TTN были успешно обновлены.'
        }))

    async def send_preorders_update(self, preorders=None, additional_event=None):
        if preorders is None:
            preorders = await self.get_filtered_preorders(self.active_filter)

        preorders_data = await sync_to_async(self.build_preorders_data)(preorders)
        counts = await self.get_preorder_counts()

        html = await sync_to_async(render_to_string)(
            'seller_cabinet/preorders/seller_preorders.html', {'preorders': preorders_data}
        ) if preorders_data and counts else None

        message = {
            'event': 'preorder_list',
            'html': html,
            'counts': counts
        }

        # Добавляем дополнительное событие, если оно есть
        if additional_event:
            message['additional_event'] = additional_event

        await self.send(text_data=json.dumps(message))

    async def search_preorders(self, search_text):
        preorders = await sync_to_async(list)(
            PreOrder.objects.filter(
                Q(ttn__icontains=search_text) |
                Q(full_name__icontains=search_text) |
                Q(text__icontains=search_text)
            ).order_by('-created_at')
        )
        return preorders

    async def get_preorder_counts(self):
        counts = {
            'all': await sync_to_async(PreOrder.objects.count)(),
            'not_shipped': await sync_to_async(PreOrder.objects.filter(shipped_to_customer=False).count)(),
            'not_receipted': await sync_to_async(PreOrder.objects.filter(receipt_issued=False).count)(),
            'not_paid': await sync_to_async(PreOrder.objects.filter(payment_received=False).count)(),
        }
        return counts

    def build_preorders_data(self, preorders):
        return [self.build_preorder_data(preorder) for preorder in preorders]

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

    async def get_filtered_preorders(self, filter_type):
        if filter_type == 'all':
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))
        elif filter_type == 'not-shipped':
            preorders = await sync_to_async(list)(
                PreOrder.objects.filter(shipped_to_customer=False).order_by('-created_at'))
        elif filter_type == 'not-receipted':
            preorders = await sync_to_async(list)(
                PreOrder.objects.filter(receipt_issued=False).order_by('-created_at'))
        elif filter_type == 'not-paid':
            preorders = await sync_to_async(list)(
                PreOrder.objects.filter(payment_received=False).order_by('-created_at'))
        else:
            preorders = await sync_to_async(list)(PreOrder.objects.all().order_by('-created_at'))

        return preorders


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

        products = []
        for r in results:
            product = await sync_to_async(lambda: r.product)()
            thumbnail_url = await sync_to_async(r.thumbnail_image_url)()
            actual_price = await sync_to_async(
                lambda: product.get_actual_wholesale_price())()  # Используем метод get_actual_wholesale_price
            products.append({
                'name': f"{product.title}-{r.custom_sku}",
                'stock': r.stock,
                'price': actual_price,
                'custom_sku': r.custom_sku,
                'thumbnail': thumbnail_url
            })

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
                    'custom_sku': custom_sku,
                    'available_stock': product_modification.stock  # Отправляем информацию о доступном остатке
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
                    'price': sale_item.total_price(),
                    'remaining_stock': product_modification.stock  # Отправляем остаток после добавления
                }))
        except ObjectDoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'item_not_available',
                'custom_sku': custom_sku
            }))

    async def create_sale(self, source, payment_method, comment, items):
        # Получаем текущего пользователя из сессии WebSocket
        user = self.scope['user']
        # Получаем TelegramUser асинхронно
        telegram_user = await sync_to_async(lambda: getattr(user, 'telegram_user', None))()
        if not telegram_user:
            await self.send(text_data=json.dumps({
                'type': 'sell_error',
                'message': f'TelegramUser associated with User ID {user.id} does not exist.'
            }))
            return

        # Создаём запись о продаже
        sale = await sync_to_async(Sale.objects.create)(
            user=user,
            telegram_user=telegram_user,
            source=source,
            payment_method=payment_method,
            comment=comment
        )

        # Добавляем товары в продажу
        for item in items:
            product_modification = await sync_to_async(ProductModification.objects.get)(custom_sku=item['custom_sku'])
            await sync_to_async(SaleItem.objects.create)(
                sale=sale,
                product_modification=product_modification,
                quantity=item['quantity']
            )

        total_amount = 0
        for item in items:
            if 'total' in item:
                total_amount += item['quantity'] * item['total']
            else:
                raise ValidationError(f"Key 'total' is missing in item: {item}")

        sale.total_amount = total_amount
        await sync_to_async(sale.save)()

        await self.send(text_data=json.dumps({
            'type': 'sell_confirmation',
            'status': 'success',
            'sale_id': sale.id,
            'user': user.username,
            'telegram_user': telegram_user.user_name
        }))

    async def send_sales_list(self):
        today = timezone.localtime(timezone.now()).date()
        sales = await sync_to_async(list)(
            Sale.objects.filter(created_at__date=today).order_by('-created_at')
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
                'created_at': timezone.localtime(sale.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                'user': await sync_to_async(lambda: sale.user.username if sale.user else 'Неизвестно')(),
                'telegram_user': await sync_to_async(
                    lambda: sale.telegram_user.user_name if sale.telegram_user else 'Неизвестно')(),
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
        # Проверяем, авторизован ли пользователь
        if self.scope["user"].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'create_return':
            await self.create_return(data)
        elif data['type'] == 'get_returns_list':
            await self.send_return_list()
        elif data['type'] == 'search':
            await self.search_items(data.get('query', ''))

    async def search_items(self, query):
        results = await sync_to_async(list)(
            ProductModification.objects.filter(custom_sku__icontains=query)
        )

        products = []
        for r in results:
            product = await sync_to_async(lambda: r.product)()
            thumbnail_url = await sync_to_async(r.thumbnail_image_url)()
            actual_price = await sync_to_async(product.get_actual_wholesale_price)()
            products.append({
                'sku': r.custom_sku,
                'stock': r.stock,
                'price': actual_price,
                'thumbnail': thumbnail_url
            })

        await self.send(text_data=json.dumps({
            'type': 'search_results',
            'results': products
        }))

    async def create_return(self, data):
        items = data['items']

        try:
            user = self.scope["user"]  # Используем пользователя из WebSocket сессии
            telegram_user = await sync_to_async(lambda: getattr(user, 'telegram_user', None))()

            if not telegram_user:
                await self.send(text_data=json.dumps({
                    'type': 'return_error',
                    'message': f'TelegramUser associated with User {user.username} does not exist.'
                }))
                return

            # Создаем возврат
            return_obj = Return(
                user=user,
                telegram_user=telegram_user,  # Привязываем TelegramUser
                comment=data['comment']
            )
            await sync_to_async(return_obj.save)()

            for item in items:
                product_modification = await sync_to_async(ProductModification.objects.get)(
                    custom_sku=item['custom_sku']
                )
                return_item = ReturnItem(
                    return_sale=return_obj,
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
        telegram_user = await sync_to_async(
            lambda: return_obj.telegram_user.user_name if return_obj.telegram_user else 'Неизвестно')()

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
            'telegram_user': telegram_user,
            'total_amount': await sync_to_async(return_obj.calculate_total_amount)(),
            'items': items_data,
            'comment': return_obj.comment
        }


class InventoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Проверяем, авторизован ли пользователь
        if self.scope["user"].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'create_inventory':
            await self.create_inventory(data)
        elif data['type'] == 'get_inventory_list':
            await self.send_inventory_list()
        elif data['type'] == 'search':
            await self.search_items(data.get('query', ''))

    async def search_items(self, query):
        results = await sync_to_async(list)(
            ProductModification.objects.filter(custom_sku__icontains=query)
        )
        products = []
        for r in results:
            product = await sync_to_async(lambda: r.product)()
            actual_price = await sync_to_async(
                product.get_actual_wholesale_price)()
            thumbnail_url = await sync_to_async(r.thumbnail_image_url)()
            products.append({
                'sku': r.custom_sku,
                'stock': r.stock,
                'price': actual_price,
                'thumbnail': thumbnail_url
            })

        await self.send(text_data=json.dumps({
            'type': 'search_results',
            'results': products
        }))

    async def create_inventory(self, data):
        items = data['items']

        try:
            user = self.scope["user"]  # Используем пользователя из WebSocket сессии
            telegram_user = await sync_to_async(lambda: getattr(user, 'telegram_user', None))()

            if not telegram_user:
                await self.send(text_data=json.dumps({
                    'type': 'inventory_error',
                    'message': f'TelegramUser associated with User {user.username} does not exist.'
                }))
                return

            # Создаем инвентаризацию
            inventory_obj = Inventory(
                user=user,
                telegram_user=telegram_user,  # Привязываем TelegramUser
                comment=data['comment']
            )
            await sync_to_async(inventory_obj.save)()

            for item in items:
                product_modification = await sync_to_async(ProductModification.objects.get)(
                    custom_sku=item['custom_sku']
                )
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
        telegram_user = await sync_to_async(
            lambda: inventory_obj.telegram_user.user_name if inventory_obj.telegram_user else 'Неизвестно')()

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
            'telegram_user': telegram_user,
            'total_amount': await sync_to_async(inventory_obj.calculate_total_amount)(),
            'items': items_data
        }


class WriteOffConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Проверяем авторизацию пользователя
        if self.scope["user"].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'create_write_off':
            await self.create_write_off(data)
        elif data['type'] == 'get_write_off_list':
            await self.send_write_off_list()
        elif data['type'] == 'search':
            await self.search_items(data.get('query', ''))

    async def search_items(self, query):
        results = await sync_to_async(list)(
            ProductModification.objects.filter(custom_sku__icontains=query)
        )
        products = []
        for r in results:
            product = await sync_to_async(lambda: r.product)()
            actual_price = await sync_to_async(product.get_actual_wholesale_price)()
            thumbnail_url = await sync_to_async(r.thumbnail_image_url)()
            products.append({
                'sku': r.custom_sku,
                'stock': r.stock,
                'price': actual_price,
                'thumbnail': thumbnail_url
            })

        await self.send(text_data=json.dumps({
            'type': 'search_results',
            'results': products
        }))

    async def create_write_off(self, data):
        items = data['items']

        try:
            user = self.scope["user"]  # Используем текущего пользователя из WebSocket сессии
            telegram_user = await sync_to_async(lambda: getattr(user, 'telegram_user', None))()

            if not telegram_user:
                await self.send(text_data=json.dumps({
                    'type': 'write_off_error',
                    'message': f'TelegramUser associated with User {user.username} does not exist.'
                }))
                return

            # Создаем списание
            write_off = await sync_to_async(WriteOff.objects.create, thread_sensitive=True)(
                user=user,
                telegram_user=telegram_user,  # Привязываем TelegramUser
                source=data['source'],
                comment=data['comment']
            )

            for item in items:
                product_modification = await sync_to_async(ProductModification.objects.get, thread_sensitive=True)(
                    custom_sku=item['custom_sku']
                )
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
        telegram_user = await sync_to_async(lambda: write_off.telegram_user.user_name if write_off.telegram_user else 'Неизвестно')()
        total_amount = await sync_to_async(write_off.calculate_total_amount)()
        items = await sync_to_async(list)(write_off.items.all())

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
            'telegram_user': telegram_user,
            'total_amount': total_amount,
            'items': items_data,
        }


class ReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.period = 'today'
        self.start_date = None
        self.end_date = None

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        if event_type == 'update_period':
            self.period = data.get('period', 'today')
            if self.period == 'custom':
                self.start_date = data.get('start_date')
                self.end_date = data.get('end_date')
            else:
                self.start_date = None
                self.end_date = None
            await self.send_report_data()
        elif event_type == 'get_initial_data':
            await self.send_report_data()
        elif event_type == 'get_stock_data':
            await self.send_stock_data()

    async def send_report_data(self):
        report_data = await self.get_report_data(self.period, self.start_date, self.end_date)

        sales_data = report_data.get('sales')
        returns_data = report_data.get('returns')
        net_data = report_data.get('net')

        await self.send(text_data=json.dumps({
            'event': 'report_data',
            'sales_data': {
                'sales': sales_data,
                'returns': returns_data,
                'net': net_data
            }
        }))

    async def send_stock_data(self):
        stock_data = await self.get_stock_data()

        await self.send(text_data=json.dumps({
            'event': 'stock_data',
            'stock_data': stock_data
        }))

    async def get_report_data(self, period, start_date=None, end_date=None):
        start_date, end_date = self.get_date_range(period, start_date, end_date)

        sales = await sync_to_async(list)(
            Sale.objects.filter(created_at__range=(start_date, end_date)).prefetch_related(
                'items__product_modification')
        )

        returns = await sync_to_async(list)(
            Return.objects.filter(created_at__range=(start_date, end_date)).prefetch_related(
                'items__product_modification')
        )

        # Добавим разделение по типам оплаты
        sales_by_payment = {'cash': 0, 'non_cash': 0}
        sales_summary, total_sales_quantity, total_sales_sum = await self.process_transactions(sales, sales_by_payment)

        returns_summary, total_returns_quantity, total_returns_sum = await self.process_transactions(returns)

        # Добавляем общие суммы в результат по продажам и возвратам
        sales_summary['total'] = {
            'total_quantity': total_sales_quantity,
            'total_sales_sum': total_sales_sum,
            'cash_sales': sales_by_payment['cash'],
            'non_cash_sales': sales_by_payment['non_cash']
        }

        returns_summary['total'] = {
            'total_quantity': total_returns_quantity,
            'total_sales_sum': total_returns_sum
        }

        # Рассчитываем чистую кассу
        net_sales_quantity = total_sales_quantity - total_returns_quantity
        net_sales_sum = total_sales_sum - total_returns_sum

        return {
            'sales': sales_summary if total_sales_quantity > 0 else None,
            'returns': returns_summary if total_returns_quantity > 0 else None,
            'net': {
                'net_sales_quantity': net_sales_quantity,
                'net_sales_sum': net_sales_sum
            }
        }

    async def get_stock_data(self):
        try:
            # Получаем все модификации продуктов с их связанными продуктами
            modifications = await sync_to_async(list)(
                ProductModification.objects.select_related('product').all()
            )

            stock_summary = {}

            for mod in modifications:
                product = await sync_to_async(lambda: mod.product)()
                product_sku = await sync_to_async(lambda: product.sku)()
                product_title = await sync_to_async(lambda: product.title)()
                modification_sku = await sync_to_async(lambda: mod.custom_sku)()
                stock_quantity = await sync_to_async(lambda: mod.stock)()

                # Получаем URL коллажей
                collage_image_url = await sync_to_async(lambda: product.collage_thumbnail.url if product.collage_thumbnail else '')()

                if product_sku not in stock_summary:
                    stock_summary[product_sku] = {
                        'product_title': product_title,
                        'collage_image_url': collage_image_url,
                        'modifications': {},
                    }

                stock_summary[product_sku]['modifications'][modification_sku] = {
                    'stock_quantity': stock_quantity,
                    'thumbnail_url': await sync_to_async(mod.thumbnail_image_url)(),
                }

            # Сортируем продукты по SKU в порядке убывания
            def extract_numeric_prefix(sku):
                match = re.match(r'^(\d+)', sku)
                if match:
                    return int(match.group(1))
                else:
                    return float('-inf')  # Для SKU без числового префикса

            sorted_stock_summary = dict(sorted(
                stock_summary.items(),
                key=lambda item: extract_numeric_prefix(item[0]),
                reverse=True
            ))

            return sorted_stock_summary
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка при получении данных по остаткам: {e}")
            return {}

    async def process_transactions(self, transactions, sales_by_payment=None):
        summary = {}
        total_quantity = 0
        total_sum = 0.0

        for transaction in transactions:
            # Определяем тип оплаты и добавляем соответствующую сумму
            if sales_by_payment is not None:
                total_amount = await sync_to_async(transaction.calculate_total_amount)()
                if transaction.payment_method == 'cash':
                    sales_by_payment['cash'] += total_amount
                else:
                    sales_by_payment['non_cash'] += total_amount

            # Получаем связанные данные через sync_to_async
            items = await sync_to_async(list)(transaction.items.all())
            for item in items:
                # Оборачиваем доступ к связанной модификации и продукту
                product_modification = await sync_to_async(lambda: item.product_modification)()
                product = await sync_to_async(lambda: product_modification.product)()

                product_sku = await sync_to_async(lambda: product.sku)()
                product_title = await sync_to_async(lambda: product.title)()
                modification_sku = await sync_to_async(lambda: product_modification.custom_sku)()
                quantity = await sync_to_async(lambda: item.quantity)()
                product_price = await sync_to_async(lambda: product.get_actual_wholesale_price())()
                item_total_price = product_price * quantity
                thumbnail_url = await sync_to_async(lambda: item.thumbnail_image_url())()
                collage_image_url = await sync_to_async(lambda: product.collage_image_url())()

                total_quantity += quantity
                total_sum += item_total_price

                if product_sku not in summary:
                    summary[product_sku] = {
                        'product_title': product_title,
                        'total_quantity': 0,
                        'collage_image_url': collage_image_url,
                        'modifications': {}
                    }

                summary[product_sku]['total_quantity'] += quantity
                if modification_sku not in summary[product_sku]['modifications']:
                    summary[product_sku]['modifications'][modification_sku] = {
                        'quantity': 0,
                        'thumbnail_url': thumbnail_url
                    }
                summary[product_sku]['modifications'][modification_sku]['quantity'] += quantity

        return summary, total_quantity, total_sum

    def get_date_range(self, period, start_date=None, end_date=None):
        now = timezone.now()

        if period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'yesterday':
            start_date = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif period == 'week':
            start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'year':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'custom':
            if not start_date or not end_date:
                raise ValueError("Отсутствуют даты для кастомного периода.")
            try:
                start_date = timezone.make_aware(datetime.strptime(start_date, '%d-%m-%Y'))
                end_date = timezone.make_aware(datetime.strptime(end_date, '%d-%m-%Y')).replace(hour=23, minute=59, second=59)
            except ValueError:
                raise ValueError("Неправильный формат дат для кастомного периода.")
        else:
            raise ValueError("Неподдерживаемый период.")

        return start_date, end_date