from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductModification, Category, Image, Color, Size

from django.db import models


class ImageAdmin(admin.ModelAdmin):
    list_display = ('modification', 'thumbnail_image')
    list_display_links = ('modification', 'thumbnail_image')
    #extra = 1

    def thumbnail_image(self, obj):
        return format_html('<img src="{}"/>', obj.thumbnail.url)

    thumbnail_image.allow_tags = True
    thumbnail_image.short_description = 'Миниатюра изображения'


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1  # Количество пустых форм для добавления изображений

    def thumbnail_image(self, obj):
        return format_html('<img src="{}"/>', obj.thumbnail.url)

    thumbnail_image.allow_tags = True
    thumbnail_image.short_description = 'Миниатюра изображения'

    fields = ('thumbnail_image', 'image')  # Добавляем миниатюру в список отображаемых полей

    readonly_fields = ('thumbnail_image',)


class ProductModificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'custom_sku', 'color', 'size', 'stock', 'price', 'currency', 'thumbnail_image')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__title', 'color__name', 'size__name', 'custom_sku')
    inlines = [ImageInline]

    def thumbnail_image(self, obj):
        images = Image.objects.filter(modification=obj)  # Получаем изображения, связанные с данной модификацией
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image.allow_tags = True
    thumbnail_image.short_description = 'Миниатюра изображения'


class ProductModificationInline(admin.TabularInline):
    model = ProductModification
    extra = 0  # Количество пустых форм для добавления модификаций
    fields = ('product', 'custom_sku', 'color', 'size', 'stock', 'price', 'currency', 'get_thumbnail_image')
    readonly_fields = ('get_thumbnail_image',)  # Добавляем метод get_thumbnail_image в readonly_fields

    def get_thumbnail_image(self, obj):
        images = Image.objects.filter(modification=obj)  # Получаем изображения, связанные с данной модификацией
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    get_thumbnail_image.allow_tags = True
    get_thumbnail_image.short_description = 'Миниатюра изображения'


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModificationInline]
    list_display = ('title', 'sku', 'category', 'description', 'get_colors', 'get_sizes', 'get_total_stock', 'price',
                    'created_at', 'thumbnail_image')
    search_fields = ('sku',)

    def get_total_stock(self, obj):
        total_stock = sum(mod.stock for mod in obj.modifications.all())
        return total_stock

    get_total_stock.short_description = 'Сумма остатков'

    def get_colors(self, obj):
        return ", ".join([color.name for color in obj.colors.all()])

    get_colors.short_description = 'Цвета'

    def get_sizes(self, obj):
        return ", ".join([size.name for size in obj.sizes.all()])

    get_sizes.short_description = 'Размеры'

    def thumbnail_image(self, obj):
        images = Image.objects.filter(modification__product=obj)  # Получаем изображения, связанные с этим товаром
        if images:
            return format_html('<img src="{}"/>', images[0].thumbnail.url)
        return format_html('<p>No Image</p>')

    thumbnail_image.allow_tags = True
    thumbnail_image.short_description = 'Миниатюра изображения'


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductModification, ProductModificationAdmin)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Image, ImageAdmin)
