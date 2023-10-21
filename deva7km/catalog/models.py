from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    colors = models.ManyToManyField('Color', blank=True, verbose_name='Цвета')
    sizes = models.ManyToManyField('Size', blank=True, verbose_name='Размеры')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'  # Название модели в единственном числе
        verbose_name_plural = 'Товары'  # Название модели во множественном числе


class ProductModification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    color = models.ForeignKey('Color', on_delete=models.CASCADE, verbose_name='Цвет')
    size = models.ForeignKey('Size', on_delete=models.CASCADE, verbose_name='Размер')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    price = models.IntegerField(default=Product.price, verbose_name='Цена')
    custom_sku = models.CharField(max_length=20, verbose_name='Артикул комплектации', blank=True)
    # Свяжем модель Image с моделью ProductModification через ManyToManyField
    images = models.ManyToManyField('Image', blank=True, verbose_name='Изображения')

    def __str__(self):
        return self.custom_sku  # Отображаем свой артикул вместо sku

    def clean(self):
        if self.stock < 0:
            raise ValidationError('Остаток не может быть отрицательным числом.')
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной.')

    class Meta:
        verbose_name = 'Модификация товара'  # Название модели в единственном числе
        verbose_name_plural = 'Модификации товаров'  # Название модели во множественном числе
        unique_together = ['product', 'color', 'size']


class Image(models.Model):
    original = models.ImageField(upload_to='images/', verbose_name='Оригинальное изображение')
    thumbnail = ImageSpecField(
        source='original',
        processors=[ResizeToFit(100, 100)],
        format='JPEG',
        options={'quality': 60},
    )

    class Meta:
        verbose_name = 'Изображение товара'  # Название модели в единственном числе
        verbose_name_plural = 'Изображения товара'  # Название модели во множественном числе


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'  # Название модели в единственном числе
        verbose_name_plural = 'Цвета'  # Название модели во множественном числе


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'  # Название модели в единственном числе
        verbose_name_plural = 'Размеры'  # Название модели во множественном числе


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


