from django.contrib import messages
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit
from unidecode import unidecode


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    colors = models.ManyToManyField('Color', blank=True, verbose_name='Цвета')
    sizes = models.ManyToManyField('Size', blank=True, verbose_name='Размеры')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Цена')
    CURRENCY_CHOICES = (
        ('UAH', 'Гривны (грн)'),
        ('USD', 'Доллары (USD)'),
        ('EUR', 'Евро (EUR)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def save(self, *args, **kwargs):
        # Транслитерируем title и sku
        title_translit = unidecode(self.title)
        sku_translit = unidecode(self.sku)
        # Создаем slug на основе транслитерированных title и sku
        self.slug = slugify(f"{title_translit} {sku_translit}")
        super(Product, self).save(*args, **kwargs)

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
    price = models.IntegerField(default=0, verbose_name='Цена')
    currency = models.CharField(max_length=3, choices=Product.CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')
    custom_sku = models.CharField(max_length=20, verbose_name='Артикул комплектации', blank=True)
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


# Модель категории товара
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def save(self, *args, **kwargs):
        # Транслитерируем name
        name_translit = unidecode(self.name)
        # Создаем slug на основе транслитерированного name
        self.slug = slugify(f"{name_translit}")
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'  # Название модели в единственном числе
        verbose_name_plural = 'Категории товара'  # Название модели во множественном числе
        ordering = ('name',)  # Сортировка по наименованию категории
        get_latest_by = 'created_at'  # Последние категории будут отображаться первыми


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


class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Основной товар')
    product_modification = models.ForeignKey('ProductModification', on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество проданных товаров', default=1)
    total_sale = models.IntegerField(verbose_name='Общая сумма продажи', default=0, editable=False)
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи', editable=False)
    sale_time = models.TimeField(auto_now_add=True, verbose_name='Время продажи', editable=False)
    currency = models.CharField(max_length=3, choices=Product.CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')
    is_processed = models.BooleanField(default=False, editable=False)  # Флаг обработки продажи

    def save(self, *args, **kwargs):
        if not self.is_processed:
            if self.product_modification.stock < self.quantity:
                raise ValidationError('Недостаточно товара на складе.')
            else:
                self.product_modification.stock -= self.quantity
                self.product_modification.save()
                self.total_sale = self.product_modification.price * self.quantity
                self.is_processed = True
                return super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.title} - {self.product_modification.custom_sku}'

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
