from django.contrib import admin
from .models import (
    Category, Color, Size, Product, ProductModification, Image, SaleItem, ReturnItem, Return,
    TelegramUser, Inventory, InventoryItem, WriteOff, WriteOffItem, Sale
)


# Модели связанные с пользователями Telegram
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'first_name', 'last_name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user_id', 'user_name', 'first_name', 'last_name')


admin.site.register(TelegramUser, TelegramUserAdmin)


# Модели для учета возвратов
class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification')


class ReturnAdmin(admin.ModelAdmin):
    inlines = [ReturnItemInline]
    list_display = (
    'get_returned_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount', 'source')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')

    # Метод для запрета на редактирование, если возврат завершен
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Return, ReturnAdmin)


# Модели для учета продаж
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ('get_sold_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')

    # Метод для запрета на редактирование, если продажа завершена
    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


admin.site.register(Sale, SaleAdmin)


# Модели для работы с изображениями и модификациями товаров
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    fields = [('image', 'thumbnail_image')]
    readonly_fields = ('thumbnail_image',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('modification', 'thumbnail_image')


class ProductModificationAdmin(admin.ModelAdmin):
    list_display = (
    'product', 'custom_sku', 'color', 'size', 'stock', 'price', 'currency', 'thumbnail_image_modification',)
    list_filter = ('color', 'size', 'custom_sku',)
    search_fields = ('product__title', 'color__name', 'size__name', 'custom_sku')
    inlines = [ImageInline]
    ordering = ['-created_at']


admin.site.register(Image, ImageAdmin)
admin.site.register(ProductModification, ProductModificationAdmin)


# Модели для учета товаров
class ProductModificationInline(admin.TabularInline):
    model = ProductModification
    extra = 0
    list_display = ('product', 'custom_sku', 'color', 'size', 'stock', 'price', 'currency',)
    readonly_fields = ('thumbnail_image_modification',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModificationInline]
    list_display = ('title', 'sku', 'category', 'description', 'get_colors', 'get_sizes', 'get_total_stock', 'price',
                    'thumbnail_image', 'created_at')
    search_fields = ('sku',)
    list_filter = ('sku', 'category', 'colors', 'sizes',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['-created_at']


admin.site.register(Product, ProductAdmin)


# Модели для учета инвентаризации
class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class InventoryAdmin(admin.ModelAdmin):
    inlines = [InventoryItemInline]
    list_display = ('get_inventory_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')

    # Метод для запрета на редактирование, если оприходование завершено
    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


admin.site.register(Inventory, InventoryAdmin)


# Модели для учета списания товаров
class WriteOffItemInline(admin.TabularInline):
    model = WriteOffItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class WriteOffAdmin(admin.ModelAdmin):
    inlines = [WriteOffItemInline]
    list_display = ('get_write_off_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')

    # Метод для запрета на редактирование, если списание завершено
    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


admin.site.register(WriteOff, WriteOffAdmin)

# Регистрация отдельных моделей
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
# ... (ваш код для остальных моделей)
