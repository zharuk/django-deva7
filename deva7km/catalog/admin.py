from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Color, Size, ProductModification, Image
from django.db import models


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class ProductModificationInline(admin.TabularInline):  # класс модификаций для встраивания в inlines
        model = ProductModification
        extra = 0

    class ImageAdminInline(admin.TabularInline):
        model = Image
        extra = 3
        readonly_fields = ('thumbnail',)

        # Метод для вывода миниатюр в ImageAdminInline
        def thumbnail(self, obj):
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="50" height="60" />')

        thumbnail.short_description = 'Миниатюра'

    list_display = ('title', 'sku', 'price', 'get_colors', 'get_sizes', 'get_stock', 'created_at', 'get_images')
    list_filter = ('colors', 'sizes', 'created_at')
    search_fields = ('title', 'sku')
    inlines = [ImageAdminInline, ProductModificationInline]

    def get_colors(self, obj):
        return ", ".join([color.name for color in obj.colors.all()])

    get_colors.short_description = 'Цвета'  # Название колонки в админке

    def get_sizes(self, obj):
        return ", ".join([size.name for size in obj.sizes.all()])

    get_sizes.short_description = 'Размеры'  # Название колонки в админке

    def get_stock(self, obj):
        total_stock = ProductModification.objects.filter(product=obj).aggregate(models.Sum('stock'))['stock__sum']
        return total_stock or 0

    get_stock.short_description = 'Остатки'  # Название колонки в админке

    def get_images(self, obj):
        # Получаем связанные изображения с товаром
        images = Image.objects.filter(product=obj)
        # Создаем HTML для вывода миниатюр
        image_html = ''.join([f'<img src="{image.thumbnail.url}" width="50" height="60" />' for image in images])
        return mark_safe(image_html)

    get_images.short_description = 'Изображения'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('path', 'thumbnail', 'product', 'get_image')

    def get_image(self, obj):
        return mark_safe(
            f'<img src="{obj.thumbnail.url}" width="50" height="60" />')  # Метод для вывода миниатюр в админке

    get_image.short_description = "Изображение"


admin.site.register(Size)
admin.site.register(Color)
