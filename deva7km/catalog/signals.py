from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch import receiver
from .models import Sale, Product, ProductModification


# When a sale is deleted, return the products to the stock.
@receiver(pre_delete, sender=Sale)
def return_products_on_delete(sender, instance, **kwargs):
    product_modification = instance.product_modification
    product_modification.stock += instance.quantity
    product_modification.save()


# When a product is added or removed from the colors or sizes, create or update the modifications.
@receiver(m2m_changed, sender=Product.colors.through)
@receiver(m2m_changed, sender=Product.sizes.through)
def update_product_modifications(sender, instance, action, model, pk_set, **kwargs):
    # если добавляем или изменяем товар - то создаем модификации для каждого цвета и размера
    if action in ['post_add', 'post_remove', 'post_clear']:
        if action in ['post_remove']:
            ProductModification.objects.filter(product=instance).delete()

        for color in instance.colors.all():
            for size in instance.sizes.all():
                custom_sku = f"{instance.sku}-{color.name}-{size.name}"
                _, _ = ProductModification.objects.update_or_create(
                    product=instance,
                    color=color,
                    size=size,
                    defaults={'price': instance.price, 'custom_sku': custom_sku}
                )
