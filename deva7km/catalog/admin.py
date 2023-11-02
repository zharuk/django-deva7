from django.contrib import admin
from .models import Product, ProductModification, Category, Image, Color, Size, SaleItem

from django.contrib import admin
from .models import Sale


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1  # Количество пустых форм для добавления SaleItem
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ('id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')


# Создаем класс ImageAdmin, настраивающий отображение модели Image в административной панели.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('modification', 'thumbnail_image')


# Создаем класс ImageInline для встраивания модели Image в административную панель ProductModification.
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1  # Количество пустых форм для добавления изображений
    fields = [('image', 'thumbnail_image')]  # Добавляем миниатюру в список отображаемых полей
    readonly_fields = ('thumbnail_image',)


# Создаем класс ProductModificationAdmin для настройки отображения модели ProductModification в административной панели.
class ProductModificationAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'custom_sku', 'color', 'size', 'stock', 'price', 'currency', 'thumbnail_image_modification',)
    list_filter = ('color', 'size', 'custom_sku',)
    search_fields = ('product__title', 'color__name', 'size__name', 'custom_sku')
    inlines = [ImageInline]  # Встраиваем ImageInline для отображения изображений внутри ProductModification.
    ordering = ['-created_at']


# Создаем класс ProductModificationInline для встраивания модели ProductModification в административную панель Product.
class ProductModificationInline(admin.TabularInline):
    model = ProductModification
    extra = 0  # Количество пустых форм для добавления модификаций
    list_display = ('product', 'custom_sku', 'color', 'size', 'stock', 'price', 'currency',)
    readonly_fields = ('thumbnail_image_modification',)


# Создаем класс ProductAdmin для настройки отображения модели Product в административной панели.
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModificationInline, ]  # Встраиваем ProductModificationInline для отображения модификаций
    # внутри Product.
    list_display = ('title', 'sku', 'category', 'description', 'get_colors', 'get_sizes', 'get_total_stock', 'price',
                    'thumbnail_image', 'created_at')
    search_fields = ('sku',)
    list_filter = ('sku', 'category', 'colors', 'sizes',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['-created_at']


# Регистрируем модели в административной панели Django.
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductModification, ProductModificationAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Sale, SaleAdmin)
