from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit
from unidecode import unidecode
from django.utils.translation import gettext_lazy as _

try:
    from deva7km.local_settings import BASE_URL
except ImportError:
    from deva7km.prod_settings import BASE_URL


# Модель товара
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    colors = models.ManyToManyField('Color', blank=True, verbose_name='Цвета')
    sizes = models.ManyToManyField('Size', blank=True, verbose_name='Размеры')
    price = models.IntegerField(default=0, verbose_name='Цена')
    sale_price = models.IntegerField(default=0, verbose_name='Цена распродажи')
    retail_price = models.IntegerField(default=0, verbose_name='Цена в розницу')
    retail_sale_price = models.IntegerField(default=0, verbose_name='Цена распродажи в розницу')
    CURRENCY_CHOICES = (
        ('UAH', 'Гривны (грн)'),
        ('USD', 'Доллары (USD)'),
        ('EUR', 'Евро (EUR)'),)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH', verbose_name='Валюта')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_sale = models.BooleanField(default=False, verbose_name='Распродажа')
    is_active = models.BooleanField(default=True, verbose_name='Включен')
    collage_image = models.ImageField(upload_to='collage_images/', null=True, blank=True,
                                      verbose_name='Коллаж изображений')
    collage_thumbnail = ImageSpecField(
        source='collage_image',
        processors=[ResizeToFit(100, 100)],
        format='JPEG',
        options={'quality': 60}
    )

    def get_actual_wholesale_price(self):
        return self.sale_price if self.sale_price > 0 else self.price

    def get_absolute_url(self):
        relative_url = reverse('product_detail', args=[self.category.slug, self.slug])
        return BASE_URL + relative_url

    def get_images_by_colors_limited(self, max_photos=9, min_per_color=2):
        """
        Возвращает список изображений с учетом лимита:
        - минимум min_per_color фото с каждого цвета
        - всего не более max_photos
        """
        seen_colors = set()
        result_images = []
        remaining_images = []

        # Получаем все модификации товара, упорядоченные по цвету
        modifications = self.modifications.select_related('color').order_by('color__name')

        for modification in modifications:
            color_name = modification.color.name

            if color_name not in seen_colors:
                seen_colors.add(color_name)

                # Все изображения этой модификации
                images = modification.get_all_large_image_urls()

                # Берем минимум min_per_color фото для каждого цвета
                result_images.extend(images[:min_per_color])

                # Остальные фото оставляем для добавления, если останутся слоты
                remaining_images.extend(images[min_per_color:])

        # Считаем сколько осталось мест до max_photos
        remaining_slots = max_photos - len(result_images)
        if remaining_slots > 0:
            result_images.extend(remaining_images[:remaining_slots])

        # Обрезаем на всякий случай
        return result_images[:max_photos]

    def large_image_url(self):
        return self.get_first_image_url('large_image')

    def get_all_large_images(self):
        return self.get_all_image_urls('large_image')

    def collage_image_url(self):
        return BASE_URL + self.collage_image.url if self.collage_image else None

    def get_collage_thumbnail(self):
        return format_html('<img src="{}" />', self.collage_thumbnail.url) if self.collage_image else 'Нет миниатюры'

    get_collage_thumbnail.short_description = 'Миниатюра коллажа'

    def save(self, *args, **kwargs):
        if self.sku and any(char.isalpha() for char in self.sku):
            self.sku = unidecode(self.sku)
        super().save(*args, **kwargs)

    def get_total_stock(self):
        """
        Подсчитывает и возвращает общее количество остатков по всем модификациям.
        Этот метод абсолютно безопасен и не сохраняет никаких изменений в базу данных.
        """
        return sum(modification.stock for modification in self.modifications.all())

    get_total_stock.short_description = 'Общие остатки'

    def get_colors(self):
        return ", ".join([color.name for color in self.colors.all()])

    get_colors.short_description = 'Цвета товара'

    def get_sizes(self):
        return ", ".join([size.name for size in self.sizes.all()])

    get_sizes.short_description = 'Размеры товара'

    def thumbnail_image(self):
        return self.get_first_image_tag('thumbnail')

    def thumbnail_image_url(self):
        return self.get_first_image_url('thumbnail')

    def get_first_image_url(self, image_type):
        images = Image.objects.filter(modification__product=self)
        if images:
            return BASE_URL + getattr(images[0], image_type).url
        return None

    def get_first_image_tag(self, image_type):
        url = self.get_first_image_url(image_type)
        return format_html('<img src="{}"/>', url) if url else format_html('<p>No Image</p>')

    def get_all_image_urls(self, image_type):
        images = Image.objects.filter(modification__product=self)
        return [BASE_URL + getattr(image, image_type).url for image in images]

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
    custom_sku = models.CharField(max_length=50, verbose_name='Артикул комплектации', blank=True)

    def thumbnail_image_modification(self):
        return self.get_first_image_tag('thumbnail')

    thumbnail_image_modification.short_description = 'Миниатюра изображения'

    def thumbnail_image_url(self):
        return self.get_first_image_url('thumbnail')

    def get_first_image_url(self, image_type):
        images = Image.objects.filter(modification=self)
        if images:
            return BASE_URL + getattr(images[0], image_type).url
        return None

    def get_first_image_tag(self, image_type):
        url = self.get_first_image_url(image_type)
        return format_html('<img src="{}"/>', url) if url else format_html('<p>No Image</p>')


    def get_all_large_image_urls(self):
        # Получаем все изображения, связанные с этой модификацией
        images = Image.objects.filter(modification=self)
        # Формируем список URL для каждого изображения
        return [BASE_URL + image.large_image.url for image in images if image.large_image]

    def total_price(self, quantity):
        product = self.product
        price = product.sale_price if product.sale_price > 0 else product.price
        return quantity * price

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
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name='Порядок'
    )

    def thumbnail_image(self):
        return format_html('<img src="{}"/>', self.thumbnail.url)

    thumbnail_image.short_description = 'Миниатюра изображения'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'
        ordering = ['order']

    def __str__(self):
        return f'{self.image}'


# Модель категории товара
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание категории')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    rz_id = models.IntegerField(default=0, verbose_name='ID категории на Rozetka')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})

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
    SOURCE_CHOICES = (
        ('site', 'Сайт'),
        ('telegram', 'telegram'))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site', verbose_name='Источник продажи')
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Статус')
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличная оплата'),
        ('non_cash', 'Безналичная оплата'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash',
                                      verbose_name='Способ оплаты')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def save(self, *args, **kwargs):
        # Просто сохраняем запись, без дополнительной логики
        super(Sale, self).save(*args, **kwargs)

    def calculate_total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    calculate_total_quantity.short_description = 'Всего товаров'

    def get_sold_items(self):
        return mark_safe("<br>".join(
            f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)"
            for item in self.items.all()
        ))

    get_sold_items.short_description = 'Проданные товары'

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
        if self.quantity > self.product_modification.stock:
            raise ValidationError(f"Недостаточно товара {self.product_modification} на остатке")

    def thumbnail_image_modification(self):
        return self.product_modification.thumbnail_image_modification()

    def thumbnail_image_url(self):
        return self.product_modification.thumbnail_image_url()

    def total_price(self):
        return self.product_modification.total_price(self.quantity)

    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент продажи #{self.id}'

    class Meta:
        verbose_name = 'Элемент продажи'
        verbose_name_plural = 'Элементы продажи'


# Модель возврата (Return)
class Return(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата возврата')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Пользователь Telegram')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    SOURCE_CHOICES = (
        ('site', 'Сайт'),
        ('telegram', 'telegram'))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site', verbose_name='Источник возврата')

    def calculate_total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    calculate_total_quantity.short_description = 'Общее количество возвращенного товара'

    def get_returned_items(self):
        return mark_safe("<br>".join(
            f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)"
            for item in self.items.all()
        ))

    get_returned_items.short_description = 'Возвращенные товары'

    def save(self, *args, **kwargs):
        # Просто сохраняем запись, без дополнительной логики
        super(Return, self).save(*args, **kwargs)

    def __str__(self):
        return f'Возврат #{self.id}'

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'


# Модель элемента возврата (ReturnItem)
class ReturnItem(models.Model):
    return_sale = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items', verbose_name='Возврат')
    product_modification = models.ForeignKey(ProductModification, on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество возвращаемого')

    def total_price(self):
        return self.product_modification.total_price(self.quantity)

    def thumbnail_image_modification(self):
        return self.product_modification.thumbnail_image_modification()

    def thumbnail_image_url(self):
        return self.product_modification.thumbnail_image_url()

    def __str__(self):
        return f'Элемент возврата #{self.id}'

    class Meta:
        verbose_name = 'Элемент возврата'
        verbose_name_plural = 'Элементы возврата'


# Модель пользователя Telegram
class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='telegram_user', verbose_name='Связь с User')
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Идентификатор пользователя telegram')
    user_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя пользователя @ telegram')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия')
    is_bot = models.BooleanField(default=False, verbose_name='Бот')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

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
        ('pending', 'В ожидании'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Статус')
    SOURCE_CHOICES = (
        ('site', 'Сайт'),
        ('telegram', 'telegram'))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site',
                              verbose_name='Источник оприходования')

    def calculate_total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    calculate_total_quantity.short_description = 'Общее количество принятого товара'

    def get_inventory_items(self):
        return mark_safe("<br>".join(
            f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)"
            for item in self.items.all()
        ))

    get_inventory_items.short_description = 'Оприходованные товары'

    def save(self, *args, **kwargs):
        # Просто сохраняем запись, без дополнительной логики
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

    def thumbnail_image_modification(self):
        return self.product_modification.thumbnail_image_modification()

    def thumbnail_image_url(self):
        return self.product_modification.thumbnail_image_url()

    def total_price(self):
        return self.product_modification.total_price(self.quantity)

    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент оприходования #{self.id}'

    class Meta:
        verbose_name = 'Элемент оприходования'
        verbose_name_plural = 'Элементы оприходования'


# Модель списания товара (WriteOff)
class WriteOff(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата списания')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Пользователь Telegram')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='Статус')
    SOURCE_CHOICES = (
        ('site', 'Сайт'),
        ('telegram', 'telegram'))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site', verbose_name='Источник списания')

    def calculate_total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    calculate_total_quantity.short_description = 'Общее количество списанного товара'

    def get_write_off_items(self):
        return mark_safe("<br>".join(
            f"{item.product_modification.product.title}-{item.product_modification.custom_sku} ({item.quantity} шт.)"
            for item in self.items.all()
        ))

    get_write_off_items.short_description = 'Списанные товары'

    def save(self, *args, **kwargs):
        # Просто сохраняем запись, без дополнительной логики
        super(WriteOff, self).save(*args, **kwargs)

    def __str__(self):
        return f'Списание товара #{self.id}'

    class Meta:
        verbose_name = 'Списание товара'
        verbose_name_plural = 'Списания товара'

# Модель элемента списания (WriteOffItem)
class WriteOffItem(models.Model):
    write_off = models.ForeignKey(WriteOff, on_delete=models.CASCADE, related_name='items',
                                  verbose_name='Списание товара')
    product_modification = models.ForeignKey('ProductModification', on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество списываемого')

    def clean(self):
        super().clean()
        if self.quantity > self.product_modification.stock:
            raise ValidationError(f"Недостаточно товара {self.product_modification} на остатке")

    def thumbnail_image_modification(self):
        return self.product_modification.thumbnail_image_modification()

    def thumbnail_image_url(self):
        return self.product_modification.thumbnail_image_url()

    def total_price(self):
        return self.product_modification.total_price(self.quantity)

    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент списания товара #{self.id}'

    class Meta:
        verbose_name = 'Элемент списания товара'
        verbose_name_plural = 'Элементы списания товара'


# Модель блога (BlogPost)
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Содержание')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def get_absolute_url(self):
        return ''

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


# Модель заказа (Order)
class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    contact_method = models.CharField(max_length=200, verbose_name='Связь с клиентом')
    delivery_method = models.CharField(max_length=200, verbose_name='Способ доставки')
    city = models.CharField(max_length=100, verbose_name='Населенный пункт')
    post_office = models.CharField(max_length=100, verbose_name='Отделение почты')
    payment_method = models.CharField(max_length=50, verbose_name='Способ оплаты')
    comment = models.TextField(verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    STATUS_CHOICES = {
        'pending': _('В ожидании'),
        'completed': _('Завершено'),
        'canceled': _('Отменено'),
    }
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.items(), default='completed', verbose_name='Статус')

    def calculate_total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    calculate_total_amount.short_description = 'Общая сумма'

    def calculate_total_retail_amount(self):
        return sum(item.retail_total_price() for item in self.items.all())

    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    calculate_total_quantity.short_description = 'Всего товаров'

    def __str__(self):
        return f'Заказ #{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# Модель элемента заказа (OrderItem)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product_modification = models.ForeignKey(ProductModification, on_delete=models.CASCADE,
                                             verbose_name='Модификация товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def clean(self):
        super().clean()
        if self.quantity > self.product_modification.stock:
            raise ValidationError(f"Недостаточно товара {self.product_modification} на остатке")

    def thumbnail_image_modification(self):
        return self.product_modification.thumbnail_image_modification()

    def thumbnail_image_url(self):
        return self.product_modification.thumbnail_image_url()

    def total_price(self):
        product = self.product_modification.product
        if product.sale_price > 0:
            return self.quantity * product.sale_price
        else:
            return self.quantity * product.price

    def retail_total_price(self):
        product = self.product_modification.product
        if product.retail_sale_price > 0:
            return self.quantity * product.retail_sale_price
        else:
            return self.quantity * product.retail_price

    def get_stock(self):
        return self.product_modification.stock

    get_stock.short_description = 'Остаток'

    def __str__(self):
        return f'Элемент заказа #{self.id}'

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'


# Модель предзаказа (PreOrder)
class PreOrder(models.Model):
    full_name = models.CharField("Имя и Фамилия", max_length=255, blank=True)
    text = models.TextField("Инфо", blank=True)
    drop = models.BooleanField("Дроп", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)
    last_modified_by = models.ForeignKey(User, verbose_name="Изменено пользователем", null=True, blank=True,
                                         on_delete=models.SET_NULL)
    receipt_issued = models.BooleanField("Чек", default=False)
    ttn = models.CharField("ТТН", max_length=30, blank=True)
    shipped_to_customer = models.BooleanField("Отправлен", default=False)
    status = models.CharField("Статус посылки", max_length=255, blank=True)
    payment_received = models.BooleanField("Оплата", default=False)

    # Новые флаги для отслеживания уведомлений
    ready_for_shipment_notified = models.BooleanField("Уведомление о готовности к отправке отправлено", default=False)
    shipped_notified = models.BooleanField("Уведомление об отправке отправлено", default=False)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        if request and request.user.is_authenticated:
            self.last_modified_by = request.user
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Предзаказ"
        verbose_name_plural = "Предзаказы"

    def __str__(self):
        return self.full_name
