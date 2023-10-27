from django.db.models.signals import pre_delete, m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from transliterate import translit
from itertools import product
from .models import Product, ProductModification, Color


# Функция для генерации слага перед сохранением товара
@receiver(pre_save, sender=Product)
def generate_product_slug(sender, instance, **kwargs):
    if not instance.slug:
        # Транслитерируем текст на кириллице и затем создаем слаг
        instance.slug = slugify(translit(instance.title, 'ru', reversed=True))


@receiver(m2m_changed, sender=Product.colors.through)
@receiver(m2m_changed, sender=Product.sizes.through)
def generate_product_modifications_on_m2m_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        colors = instance.colors.all()
        sizes = instance.sizes.all()
        existing_modifications = ProductModification.objects.filter(product=instance)

        # Получаем все возможные комбинации цветов и размеров
        combinations = list(product(colors, sizes))

        for color, size in combinations:
            if not any(mod.color == color and mod.size == size for mod in existing_modifications):
                # Создаем модификацию, если такой комбинации еще нет
                modification = ProductModification(
                    product=instance,
                    color=color,
                    size=size,
                    stock=0,  # Установите начальный остаток по вашему усмотрению
                    price=instance.price,  # Установите начальную цену по вашему усмотрению
                    currency=instance.currency,
                    custom_sku=f"{instance.sku}-{color.name}-{size.name}",
                )
                modification.save()