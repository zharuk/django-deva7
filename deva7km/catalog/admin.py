from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Color, Size, ProductModification, Image
from django.db import models


# Пропишем админку для модели Image
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('original', 'get_thumbnail')

    # вывод миниатюры изображения
    def get_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}"')

    # название колонки в админке
    get_thumbnail.short_description = 'Миниатюра'


# Пропишем админку для модели ProductModification
@admin.register(ProductModification)
class ProductModificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'custom_sku', 'color', 'size', 'stock', 'get_thumbnail', 'price')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__title', 'custom_sku')

    # метод получения миниатюр для модификаций товара
    def get_thumbnail(self, obj):
        # соберем циклом все изображения модификации товара и выведем их в админке
        images = ""
        i = 0
        for image in obj.images.all():
            images += f'<img src="{image.thumbnail.url}"> '
            i += 1
            # если i красно 5 перенос <br>
            if i % 6 == 0:
                images += '<br>'
        return mark_safe(images)

    get_thumbnail.short_description = 'Миниатюры'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # модель ProductModificationInline для отображения модели ProductModification в админке
    class ProductModificationInline(admin.TabularInline):
        model = ProductModification
        extra = 0

        # метод для отображения миниатюр изображения комплектации
        def get_thumbnail(self, obj):
            # соберем циклом все изображения модификации товара и выведем их в админке
            images = ""
            i = 0
            for image in obj.images.all():
                images += f'<img src="{image.thumbnail.url}"> '
                i += 1
                # если i красно 5 перенос <br>
                if i % 5 == 0:
                    images += '<br>'
            return mark_safe(images)

        get_thumbnail.short_description = 'Миниатюра'
        readonly_fields = ('get_thumbnail',)
        fields = ('color', 'size', 'stock', 'images', 'get_thumbnail', 'price')

    list_display = ('title', 'sku', 'price', 'get_colors', 'get_sizes', 'get_stock', 'created_at', 'get_images')
    list_filter = ('colors', 'sizes', 'created_at')
    search_fields = ('title', 'sku')
    inlines = [ProductModificationInline]

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

    # выводим миниатюры основного товара, по одной миниатюре для каждой модификации товара
    def get_images(self, obj):
        images = ""
        for mod in obj.productmodification_set.all():
            # если изображений нет, то пропускаем
            if not mod.images.all():
                continue
            images += f'<img src="{mod.images.all()[0].thumbnail.url}"> '
        return mark_safe(images)


admin.site.register(Size)
admin.site.register(Color)
