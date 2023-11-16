from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F
from django.http import request
from django.utils import timezone
from django.utils.html import format_html, linebreaks
from django.utils.safestring import mark_safe
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit
from PIL import Image as PILImage, ImageDraw


# Модель товара
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    colors = models.ManyToManyField('Color', blank=True, verbose_name='Цвета')
    sizes = models.ManyToManyField('Size', blank=True, verbose_name='Размеры')
    price = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name='Цена')
    CURRENCY_CHOICES = (
        ('UAH', 'Гривны (грн)'),
        ('USD', 'Доллары (USD)'),
        ('EUR', 'Евро (EUR)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Включен')

    # Метод для получения общего остатка товара
    def get_total_stock(self):
        total_stock = 0
        for modification in self.modifications.all():
            total_stock += modification.stock
        return total_stock

    get_total_stock.short_description = 'Общие остатки'

    # Метод для получения цветов товара в виде строки
    def get_colors(self):
        return ", ".join([color.name for color in self.colors.all()])

    get_colors.short_description = 'Цвета товара'

    # Метод для получения размеров товара в виде строки
    def get_sizes(self):
        return ", ".join([size.name for size in self.sizes.all()])

    get_sizes.short_description = 'Размеры товара'

    # Метод для отображения миниатюры изображения товара
    def thumbnail_image(self):
        images = Image.objects.filter(modification__product=self)
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image.short_description = 'Миниатюра изображения'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# Модель модификации товара
class ProductModification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар', related_name='modifications')
    color = models.ForeignKey('Color', on_delete=models.CASCADE, verbose_name='Цвет')
    size = models.ForeignKey('Size', on_delete=models.CASCADE, verbose_name='Размер')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    price = models.IntegerField(default=0, verbose_name='Цена')
    currency = models.CharField(max_length=3, choices=Product.CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')
    custom_sku = models.CharField(max_length=30, verbose_name='Артикул комплектации', blank=True)
    slug = models.SlugField(max_length=200, unique=False, blank=True, verbose_name='Слаг модификации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Включен')

    # Метод для отображения миниатюры изображения модификации товара
    def thumbnail_image_modification(self):
        images = Image.objects.filter(modification=self)
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image_modification.short_description = 'Миниатюра изображения'

    # Метод для получения ссылки на миниатюру изображения модификации товара
    def thumbnail_image_modification_url(self):
        images = Image.objects.filter(modification=self)
        if images:
            return images[0].thumbnail.url
        return None

    # Метод для получения ссылки на изображение большого размера модификации товара
    def large_image_modification_url(self):
        images = Image.objects.filter(modification=self)
        if images:
            return images[0].large_image.url
        return None

    def __str__(self):
        return f"{self.custom_sku}"

    class Meta:
        verbose_name = 'Модификация товара'
        verbose_name_plural = 'Модификации товаров'
        unique_together = ['product', 'color', 'size']


# Модель изображения товара
class Image(models.Model):
    modification = models.ForeignKey('ProductModification', on_delete=models.CASCADE,
                                     verbose_name='Модификация товара', related_name='images')
    image = models.ImageField(upload_to='images/', verbose_name='Оригинальное изображение')
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(100, 100)],
        format='JPEG',
        options={'quality': 60},
    )
    large_image = ImageSpecField(
        source='image',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 90}
    )

    # Метод для отображения миниатюры изображения
    def thumbnail_image(self):
        return format_html('<img src="{}"/>', self.thumbnail.url)

    thumbnail_image.allow_tags = True
    thumbnail_image.short_description = 'Миниатюра изображения'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'

    def __str__(self):
        return f'{self.image}'


# Модель категории товара
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'
        ordering = ('name',)
        get_latest_by = 'created_at'


# Модель цвета товара
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']


# Модель размера товара
class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['name']


# Модель продажи (Sale)
class Sale(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Пользователь Telegram')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),  # Статус "В ожидании"
        ('completed', 'Завершено'),  # Статус "Завершено"
        ('canceled', 'Отменено'))  # Статус "Отменено"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Статус')
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличная оплата'),
        ('non_cash', 'Безналичная оплата'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash',
                                      verbose_name='Способ оплаты')
    SOURCE_CHOICES = (
        ('site', 'Сайт'),
        ('telegram', 'telegram'))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site', verbose_name='Источник продажи')

    def calculate_total_amount(self):
        total_amount = 0
        currency = ''
        for item in self.items.all():
            total_amount += item.quantity * item.product_modification.price
            currency = item.product_modification.currency
        return f'{total_amount} {currency}'

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        total_quantity = 0
        for item in self.items.all():
            total_quantity += item.quantity
        return total_quantity

    calculate_total_quantity.short_description = 'Общее количество проданного товара'

    def get_sold_items(self):
        sold_items = []
        for item in self.items.all():
            sold_items.append(
                f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)<br>")
        return mark_safe("\n".join(sold_items))

    get_sold_items.short_description = 'Проданные товары'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Если объект Sale ещё не сохранен (не имеет primary key), создадим его
            super(Sale, self).save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return f'Продажа #{self.id}'

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'


# Модель элемента продажи (SaleItem)
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name='Продажа')
    product_modification = models.ForeignKey('ProductModification', on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество продаваемого')

    def clean(self):
        super().clean()

        # Проверяем наличие достаточного количества товара на остатке
        product_modification = self.product_modification
        if self.quantity > product_modification.stock:
            raise ValidationError(f"Недостаточно товара {product_modification} на остатке")

    # Метод для отображения миниатюры изображения модификации товара
    def thumbnail_image_modification(self):
        images = Image.objects.filter(modification=self.product_modification)
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image_modification.short_description = 'Миниатюра изображения'

    def total_price(self):
        return self.quantity * self.product_modification.price

    total_price.short_description = 'Сумма'

    # метод получения остатка товара
    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент продажи #{self.id}'

    class Meta:
        verbose_name = 'Элемент продажи'
        verbose_name_plural = 'Элементы продажи'


class Return(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата возврата')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Пользователь Telegram')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    SOURCE_CHOICES = (
        ('site', 'Сайт'),
        ('telegram', 'telegram'))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site', verbose_name='Источник продажи')

    def calculate_total_amount(self):
        total_amount = 0
        currency = ''
        for item in self.items.all():
            total_amount += item.quantity * item.product_modification.price
            currency = item.product_modification.currency
        return f'{total_amount} {currency}'

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        total_quantity = 0
        for item in self.items.all():
            total_quantity += item.quantity
        return total_quantity

    calculate_total_quantity.short_description = 'Общее количество возвращенного товара'

    def get_returned_items(self):
        returned_items = []
        for item in self.items.all():
            returned_items.append(
                f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)<br>")
        return mark_safe("\n".join(returned_items))

    get_returned_items.short_description = 'Возвращенные товары'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Если объект Return ещё не сохранен (не имеет primary key), создадим его
            super(Return, self).save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super(Return, self).save(*args, **kwargs)

    def __str__(self):
        return f'Возврат #{self.id}'

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'


class ReturnItem(models.Model):
    return_sale = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items', verbose_name='Возврат')
    product_modification = models.ForeignKey(ProductModification, on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество возвращаемого')

    def total_price(self):
        return self.quantity * self.product_modification.price

    total_price.short_description = 'Сумма возврата'

    # Метод для отображения миниатюры изображения модификации товара
    def thumbnail_image_modification(self):
        images = Image.objects.filter(modification=self.product_modification)
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image_modification.short_description = 'Миниатюра изображения'

    def __str__(self):
        return f'Элемент возврата #{self.id}'

    class Meta:
        verbose_name = 'Элемент возврата'
        verbose_name_plural = 'Элементы возврата'


# модель пользователя Telegram
class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name='Идентификатор пользователя')
    user_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия')
    is_bot = models.BooleanField(default=False, verbose_name='Бот')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    # Добавляем поле для выбора роли
    ROLE_CHOICES = [
        ('admin', 'Админ'),
        ('seller', 'Продавец'),
        ('unauthorized', 'Неавторизованный')
    ]
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='unauthorized', verbose_name='Роль')

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.last_name else self.first_name

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'


# Модель оприходования товара (Inventory)
class Inventory(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата оприходования')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Пользователь Telegram')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),  # Статус "В ожидании"
        ('completed', 'Завершено'),  # Статус "Завершено"
        ('canceled', 'Отменено'))  # Статус "Отменено"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Статус')

    def calculate_total_amount(self):
        total_amount = 0
        currency = ''
        for item in self.items.all():
            total_amount += item.quantity * item.product_modification.price
            currency = item.product_modification.currency
        return f'{total_amount} {currency}'

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        total_quantity = 0
        for item in self.items.all():
            total_quantity += item.quantity
        return total_quantity

    calculate_total_quantity.short_description = 'Общее количество принятого товара'

    # получение принятых товаров
    def get_inventory_items(self):
        inventory_items = []
        for item in self.items.all():
            inventory_items.append(
                f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)<br>")
        return mark_safe("\n".join(inventory_items))

    get_inventory_items.short_description = 'Проданные товары'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Если объект Sale ещё не сохранен (не имеет primary key), создадим его
            super(Inventory, self).save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super(Inventory, self).save(*args, **kwargs)

    def __str__(self):
        return f'Оприходование #{self.id}'

    class Meta:
        verbose_name = 'Оприходование'
        verbose_name_plural = 'Оприходования'


# Модель элемента оприходования (InventoryItem)
class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items',
                                  verbose_name='Оприходование')
    product_modification = models.ForeignKey('ProductModification', on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество оприходуемого')

    def clean(self):
        super().clean()

    # Метод для отображения миниатюры изображения модификации товара
    def thumbnail_image_modification(self):
        images = Image.objects.filter(modification=self.product_modification)
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image_modification.short_description = 'Миниатюра изображения'

    # метод получения общей цены принятых товаров
    def total_price(self):
        return self.quantity * self.product_modification.price

    total_price.short_description = 'Сумма'

    # метод получения остатка товара
    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент оприходования #{self.id}'

    class Meta:
        verbose_name = 'Элемент оприходования'
        verbose_name_plural = 'Элементы оприходования'


class WriteOff(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата списания')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Пользователь Telegram')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),  # Статус "В ожидании"
        ('completed', 'Завершено'),  # Статус "Завершено"
        ('canceled', 'Отменено'))  # Статус "Отменено"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Статус')

    def calculate_total_amount(self):
        total_amount = 0
        currency = ''
        for item in self.items.all():
            total_amount += item.quantity * item.product_modification.price
            currency = item.product_modification.currency
        return f'{total_amount} {currency}'

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        total_quantity = 0
        for item in self.items.all():
            total_quantity += item.quantity
        return total_quantity

    calculate_total_quantity.short_description = 'Общее количество списанного товара'

    def get_write_off_items(self):
        write_off_items = []
        for item in self.items.all():
            write_off_items.append(
                f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)<br>")
        return mark_safe("\n".join(write_off_items))

    get_write_off_items.short_description = 'Списанные товары'

    def save(self, *args, **kwargs):
        if not self.pk:
            super(WriteOff, self).save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super(WriteOff, self).save(*args, **kwargs)

    def __str__(self):
        return f'Списание товара #{self.id}'

    class Meta:
        verbose_name = 'Списание товара'
        verbose_name_plural = 'Списания товара'


class WriteOffItem(models.Model):
    write_off = models.ForeignKey(WriteOff, on_delete=models.CASCADE, related_name='items',
                                  verbose_name='Списание товара')
    product_modification = models.ForeignKey('ProductModification', on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество списываемого')

    def clean(self):
        super().clean()

        # Проверяем наличие достаточного количества товара на остатке
        product_modification = self.product_modification
        if self.quantity > product_modification.stock:
            raise ValidationError(f"Недостаточно товара {product_modification} на остатке")

    def thumbnail_image_modification(self):
        images = Image.objects.filter(modification=self.product_modification)
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image_modification.short_description = 'Миниатюра изображения'

    def total_price(self):
        return self.quantity * self.product_modification.price

    total_price.short_description = 'Сумма'

    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент списания товара #{self.id}'

    class Meta:
        verbose_name = 'Элемент списания товара'
        verbose_name_plural = 'Элементы списания товара'
