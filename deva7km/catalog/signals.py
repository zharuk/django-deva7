import logging
import time

import pytz
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import m2m_changed, post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils import timezone, formats
from django.utils.text import slugify
from transliterate import translit
from itertools import product
from unidecode import unidecode
from .models import Product, ProductModification, Image, Category, Sale, SaleItem, ReturnItem, Return, InventoryItem, \
    Inventory, WriteOffItem, WriteOff, BlogPost, PreOrder


# сигнал который устанавливает атрибут is_sale для товара если sale_price > 0, иначе False.
@receiver(pre_save, sender=Product)
def set_is_sale(sender, instance, **kwargs):
    if instance.sale_price > 0 or instance.retail_sale_price > 0:
        instance.is_sale = True
    else:
        instance.is_sale = False


# метод для списания, вычитающий остаток
@receiver(post_save, sender=WriteOffItem)
def update_stock_write_off(sender, instance, **kwargs):
    product_modification = instance.product_modification
    product_modification.stock -= instance.quantity
    product_modification.save()


# Общий обработчик для обновления остатков товара при продаже
@receiver([post_save, post_delete], sender=SaleItem)
def update_or_restore_stock(sender, instance, **kwargs):
    product_modification = instance.product_modification

    if kwargs.get('created', False):
        # Если товар добавлен в корзину, уменьшаем количество на складе
        product_modification.stock -= instance.quantity
    elif kwargs.get('signal') == post_delete:
        # Если товар удален из корзины, увеличиваем количество на складе
        product_modification.stock += instance.quantity
    else:
        # Если это обновление объекта, ничего не делаем
        return

    product_modification.save()


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


# #метод для возврата остатка при удалении продажи
# @receiver(pre_delete, sender=Sale)
# def return_stock_on_delete(sender, instance, **kwargs):
#     print(2)
#     for item in instance.items.all():
#         product_modification = item.product_modification
#         product_modification.stock += item.quantity
#         product_modification.save()


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


def format_ttn(ttn):
    ttn = ttn.replace(" ", "")  # Удаляем все пробелы
    formatted_ttn = " ".join([ttn[i:i + 4] for i in range(0, len(ttn), 4)])
    return formatted_ttn


@receiver(pre_save, sender=PreOrder)
def format_ttn_before_save(sender, instance, **kwargs):
    if instance.ttn:
        instance.ttn = format_ttn(instance.ttn)


@receiver(post_save, sender=PreOrder)
def preorder_saved(sender, instance, created, **kwargs):
    request = kwargs.get('request')
    if request and request.user.is_authenticated:
        instance.last_modified_by = request.user
        instance.save(update_fields=['last_modified_by'])

    event_type = 'preorder_saved' if created else 'preorder_updated'
    notify_preorder_change(sender=PreOrder, instance=instance, event_type=event_type)


@receiver(post_delete, sender=PreOrder)
def preorder_deleted(sender, instance, **kwargs):
    notify_preorder_change(sender=PreOrder, instance=instance, event_type='preorder_deleted')


def notify_preorder_change(sender, instance, event_type, **kwargs):
    channel_layer = get_channel_layer()

    created_at_local = timezone.localtime(instance.created_at)
    updated_at_local = timezone.localtime(instance.updated_at)
    created_at_formatted = formats.date_format(created_at_local, 'DATETIME_FORMAT')
    updated_at_formatted = formats.date_format(updated_at_local, 'DATETIME_FORMAT')
    last_modified_by = instance.last_modified_by.username if instance.last_modified_by else 'N/A'

    data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'text': instance.text,
        'drop': instance.drop,
        'created_at': created_at_formatted,
        'updated_at': updated_at_formatted,
        'receipt_issued': instance.receipt_issued,
        'shipped_to_customer': instance.shipped_to_customer,
        'payment_received': instance.payment_received,
        'status': instance.status,
        'ttn': instance.ttn,
        'last_modified_by': last_modified_by
    }

    async_to_sync(channel_layer.group_send)(
        'preorder_updates',
        {
            'type': 'notify_preorders_update',
            'event': event_type,
            'preorder': data,
        }
    )