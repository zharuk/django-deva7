from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import m2m_changed, post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.html import escape
from django.utils.text import slugify
from transliterate import translit
from itertools import product
from unidecode import unidecode

from tg_bot.bot import bot
from .models import Product, ProductModification, Image, Category, Sale, SaleItem, ReturnItem, Return, InventoryItem, \
    Inventory, WriteOffItem, WriteOff, BlogPost, PreOrder, TelegramUser
from .utils import format_ttn, notify_preorder_change


@receiver(post_save, sender=Product)
def update_product_flags(sender, instance, created, **kwargs):
    """
    Обновляет флаги is_sale и is_active после сохранения продукта.
    """
    is_sale = bool(instance.sale_price > 0 or instance.retail_sale_price > 0)
    is_active = instance.get_total_stock() > 0 if instance.pk else False

    # Чтобы избежать лишних сигналов — обновляем только если изменилось
    if instance.is_sale != is_sale or instance.is_active != is_active:
        Product.objects.filter(pk=instance.pk).update(
            is_sale=is_sale,
            is_active=is_active
        )


def update_product_is_active(product):
    """
    Проверяем суммарный остаток по всем модификациям и обновляем is_active.
    """
    total_stock = product.get_total_stock()
    product.is_active = total_stock > 0
    # используем update, чтобы не зациклить сигналы
    Product.objects.filter(pk=product.pk).update(is_active=product.is_active)

@receiver(post_save, sender=ProductModification)
def product_modification_saved(sender, instance, **kwargs):
    update_product_is_active(instance.product)

@receiver(post_delete, sender=ProductModification)
def product_modification_deleted(sender, instance, **kwargs):
    update_product_is_active(instance.product)


# метод для списания, вычитающий остаток
@receiver(post_save, sender=WriteOffItem)
def update_stock_write_off(sender, instance, **kwargs):
    product_modification = instance.product_modification
    product_modification.stock -= instance.quantity
    product_modification.save()


# метод для продажи, вычитающий остаток и отправляющий уведомление
@receiver(post_save, sender=SaleItem)
def update_sale_add_to_stock(sender, instance, **kwargs):
    product_modification = instance.product_modification
    product_modification.stock -= instance.quantity
    product_modification.save()

    # Проверяем, если остаток товара стал равен нулю
    if product_modification.stock == 0:
        user_ids = list(
            TelegramUser.objects.filter(role__in=['admin', 'seller'])
            .values_list('telegram_id', flat=True)
        )

        # Формируем текст сообщения
        message_text = (
            f"❗️ Товар {escape(product_modification.custom_sku)} "
            f"был полностью продан!"
        )

        # Отправляем сообщение через Telegram
        async def send_message(user_id, message_text):
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=message_text,
                    parse_mode='HTML'
                )
                print(f"Message sent to Telegram user ID: {user_id}")
            except Exception as e:
                print(f"Failed to send message to user ID {user_id}: {e}")

        async def send_messages(message_text):
            for user_id in user_ids:
                await send_message(user_id, message_text)

        if user_ids and message_text:
            async_to_sync(send_messages)(message_text)
        else:
            print("No users to notify or message text is missing.")


# метод для возврата остатка при возврате
@receiver(post_save, sender=ReturnItem)
def add_to_stock(sender, instance, **kwargs):
    product_modification = instance.product_modification
    product_modification.stock += instance.quantity
    product_modification.save()


# Метод для оприходования, вычитающий остаток
@receiver(post_save, sender=InventoryItem)
def update_stock_inventory(sender, instance, **kwargs):
    product_modification = instance.product_modification
    product_modification.stock += instance.quantity
    product_modification.save()


# метод для возврата остатка при удалении продажи
@receiver(pre_delete, sender=Sale)
def return_stock_on_delete(sender, instance, **kwargs):
    for item in instance.items.all():
        product_modification = item.product_modification
        product_modification.stock += item.quantity
        product_modification.save()


#  метод для возврата остатка при удалении возврата
@receiver(pre_delete, sender=Return)
def return_stock_on_delete_return(sender, instance, **kwargs):
    for item in instance.items.all():
        product_modification = item.product_modification
        product_modification.stock -= item.quantity
        product_modification.save()


# Метод для возврата остатка при удалении оприходования
@receiver(pre_delete, sender=Inventory)
def return_stock_on_delete_inventory(sender, instance, **kwargs):
    for item in instance.items.all():
        product_modification = item.product_modification
        product_modification.stock -= item.quantity
        product_modification.save()


# метод для возврата остатка при удалении списания
@receiver(pre_delete, sender=WriteOff)
def return_stock_on_delete_write_off(sender, instance, **kwargs):
    for item in instance.items.all():
        product_modification = item.product_modification
        product_modification.stock += item.quantity
        product_modification.save()


# Сигнал для генерации slug для модели Product
@receiver(pre_save, sender=Product)
def generate_product_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug_base = slugify(translit(instance.title, 'ru', reversed=True))
        instance.slug = f"{slug_base}-{instance.sku}"


# Сигнал для генерации slug для модели Category
@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug_base = slugify(unidecode(instance.name))
        instance.slug = slug_base


# Сигнал для генерации slug для модели BlogPost
@receiver(pre_save, sender=BlogPost)
def generate_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug_base = slugify(unidecode(instance.title))
        instance.slug = slug_base


# Функция для добавления всех изображений для модификаций одного и того же цвета
@receiver(post_save, sender=Image)
def associate_images_with_same_color(sender, instance, **kwargs):
    # Проверяем, было ли изображение изменено (например, при сортировке)
    if kwargs.get('update_fields') is not None:
        return

    # Получите модификацию товара, к которой относится данное изображение
    modification = instance.modification
    # Получите цвет данной модификации
    color = modification.color
    # Получите основной товар (Product), к которому относится данная модификация
    product = modification.product
    # Найдите все другие модификации этого товара с таким же цветом, исключая текущую
    other_modifications = ProductModification.objects.filter(product=product, color=color).exclude(pk=modification.pk)
    # Создайте список изображений для связывания
    images_to_create = []

    for other_modification in other_modifications:
        # Проверяем, не существует ли уже изображение в данной модификации
        existing_image = Image.objects.filter(modification=other_modification, image=instance.image).first()
        if not existing_image:
            # Создайте новый объект Image, но не сохраняйте его в базе данных
            new_image = Image(modification=other_modification, image=instance.image)
            images_to_create.append(new_image)

    # Используйте bulk_create для создания всех изображений одновременно
    Image.objects.bulk_create(images_to_create)


# Сигнал для генерации модификаций для товара
@receiver(m2m_changed, sender=Product.colors.through)
@receiver(m2m_changed, sender=Product.sizes.through)
def generate_product_modifications_on_m2m_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ["post_add", "post_remove"]:
        colors = instance.colors.all()
        sizes = instance.sizes.all()
        existing_modifications = ProductModification.objects.filter(product=instance)

        # Получаем все возможные комбинации цветов и размеров
        combinations = list(product(colors, sizes))

        if action == "post_add":
            for color, size in combinations:
                if not any(mod.color == color and mod.size == size for mod in existing_modifications):
                    # Создаем модификацию, если такой комбинации еще нет
                    modification = ProductModification(
                        product=instance,
                        color=color,
                        size=size,
                        stock=0,  # Установите начальный остаток по вашему усмотрению
                        custom_sku=f"{instance.sku}-{color.name}-{size.name}",
                    )
                    modification.save()
        elif action == "post_remove":
            for mod in existing_modifications:
                if mod.color not in colors or mod.size not in sizes:
                    # Удаляем модификацию, если цвет или размер больше не связаны с товаром
                    mod.delete()


@receiver(pre_save, sender=PreOrder)
def format_ttn_before_save(sender, instance, **kwargs):
    if instance.ttn:
        instance.ttn = format_ttn(instance.ttn)


@receiver(post_save, sender=PreOrder)
def preorder_saved(sender, instance, created, **kwargs):
    user_ids = list(
        TelegramUser.objects.filter(role__in=['admin', 'seller'])
        .values_list('telegram_id', flat=True)
    )

    channel_layer = get_channel_layer()
    message_text = None
    event_type = None

    if created:
        event_type = 'preorder_saved'
        message_text = (
            f"<b>Создан предзаказ №{instance.id}</b>\n\n"
            f"{escape(instance.full_name)}\n\n"
            f"{escape(instance.text)}\n\n"
            f"Дроп: {'✅' if instance.drop else '❌'}\n"
            f"Оплата: {'✅' if instance.payment_received else '❌'}\n\n"
            f"Создан: {instance.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"Изменено пользователем: {instance.last_modified_by.username if instance.last_modified_by else 'Неизвестно'}\n"
        )
    else:
        if instance.ttn and instance.receipt_issued and instance.payment_received:
            if instance.shipped_to_customer and not instance.shipped_notified:
                event_type = 'preorder_shipped'
                message_text = (
                    f"<b>Предзаказ №{instance.id} ({escape(instance.full_name)}) отправлен {instance.last_modified_by.username if instance.last_modified_by else 'Неизвестно'} ✅!</b>"
                )
                instance.shipped_notified = True
                instance.save(update_fields=['shipped_notified'])
            elif not instance.shipped_to_customer and not instance.ready_for_shipment_notified:
                event_type = 'preorder_updated'
                message_text = (
                    f"<b>Предзаказ №{instance.id} готов к отправке!</b>\n\n"
                    f"{escape(instance.full_name)}\n\n"
                    f"{escape(instance.text)}\n\n"
                    f"Дроп: {'✅' if instance.drop else '❌'}\n"
                    f"Оплата: {'✅' if instance.payment_received else '❌'}\n"
                    f"Чек: {'✅' if instance.receipt_issued else '❌'}\n"
                    f"Отправлен: {'✅' if instance.shipped_to_customer else '❌'}\n\n"
                    f"ТТН: <code>{escape(instance.ttn)}</code>\n\n"
                    f"Создан: {instance.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
                    f"Последний раз изменен: {instance.last_modified_by.username if instance.last_modified_by else 'Неизвестно'}"
                )
                instance.ready_for_shipment_notified = True
                instance.save(update_fields=['ready_for_shipment_notified'])

    if event_type and message_text:
        async_to_sync(channel_layer.group_send)(
            'preorder_updates',
            {
                'type': 'notify_preorders_update',
                'event': event_type,
                'preorder_id': instance.id
            }
        )

        async def send_message(user_id, message_text):
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=message_text,
                    parse_mode='HTML'
                )
                print(f"Message sent to Telegram user ID: {user_id}")
            except Exception as e:
                print(f"Failed to send message to user ID {user_id}: {e}")

        async def send_messages(message_text):
            for user_id in user_ids:
                await send_message(user_id, message_text)

        if user_ids and message_text:
            async_to_sync(send_messages)(message_text)
        else:
            print("No users to notify or message text is missing.")


@receiver(post_delete, sender=PreOrder)
def preorder_deleted(sender, instance, **kwargs):
    # Оповещение всех подключенных клиентов
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'preorder_updates',
        {
            'type': 'notify_preorders_update',
            'event': 'preorder_deleted',
            'preorder_id': instance.id
        }
    )

    notify_preorder_change(sender=PreOrder, instance=instance, event_type='preorder_deleted')
