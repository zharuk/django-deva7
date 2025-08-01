from adminsortable2.admin import SortableAdminMixin, SortableStackedInline
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.urls import path
from modeltranslation.admin import TranslationAdmin

from deva7km import settings
from .management.commands.update_tracking_status import update_tracking_status
from .models import (
    Category, Color, Size, Product, ProductModification, Image, SaleItem, ReturnItem, Return,
    TelegramUser, Inventory, InventoryItem, WriteOff, WriteOffItem, Sale, BlogPost, Order, OrderItem, PreOrder
)
from .generate_xlsx import generate_product_xlsx


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'user_name', 'first_name', 'last_name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('telegram_id', 'user_name', 'first_name', 'last_name')
    list_per_page = 25


class TelegramUserInline(admin.StackedInline):
    model = TelegramUser
    can_delete = False
    verbose_name_plural = 'Telegram User'
    fk_name = 'user'
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [TelegramUserInline]

    list_display = ('username', 'email', 'first_name', 'last_name', 'telegram_user')

    def telegram_user(self, obj):
        return obj.telegram_user.first_name if obj.telegram_user else 'Нет данных'

    telegram_user.short_description = 'Имя пользователя Telegram'


class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification')


class ReturnAdmin(admin.ModelAdmin):
    inlines = [ReturnItemInline]
    list_display = (
        'get_returned_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount', 'comment',
        'source')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')
    list_per_page = 25

    def has_change_permission(self, request, obj=None):
        if obj and hasattr(obj, 'status') and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


class ReturnItemAdmin(admin.ModelAdmin):
    list_display = ('return_sale', 'product_modification', 'quantity', 'thumbnail_image_modification')


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = (
        'get_sold_items', 'id', 'created_at', 'calculate_total_quantity', 'payment_method', 'source', 'status',
        'comment', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')
    list_per_page = 25

    # def has_change_permission(self, request, obj=None):
    #     if obj and obj.status == 'completed':
    #         return False
    #     return super().has_change_permission(request, obj)


class ImageInline(SortableStackedInline):
    model = Image
    extra = 1
    fields = [('image', 'thumbnail_image')]
    readonly_fields = ('thumbnail_image',)


class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('modification', 'thumbnail_image')
    list_per_page = 25
    search_fields = ['modification__custom_sku']


class ProductModificationAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        'product', 'custom_sku', 'color', 'size', 'stock',
        'thumbnail_image_modification',)
    list_filter = ('color', 'size', 'custom_sku',)
    search_fields = ('product__title', 'color__name', 'size__name', 'custom_sku')
    inlines = [ImageInline]
    ordering = ['product']
    list_per_page = 25


class ProductModificationInline(admin.TabularInline):
    model = ProductModification
    extra = 0
    readonly_fields = ('thumbnail_image_modification',)


class ProductAdmin(TranslationAdmin):
    inlines = [ProductModificationInline]
    list_display = (
        'title', 'sku', 'category', 'get_colors', 'get_sizes', 'get_total_stock', 'price',
        'sale_price', 'retail_price', 'retail_sale_price', 'get_collage_thumbnail', 'created_at'
    )
    search_fields = ('sku', 'title')
    list_filter = ('sku', 'category', 'colors', 'sizes',)
    readonly_fields = ('get_collage_thumbnail', 'created_at', 'updated_at',)
    ordering = ['-created_at']
    list_per_page = 25

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-products-xlsx/', self.admin_site.admin_view(self.export_products_xlsx),
                 name='export-products-xlsx'),
        ]
        return custom_urls + urls

    def export_products_xlsx(self, request):
        return generate_product_xlsx()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_products_xlsx_url'] = 'export-products-xlsx/'
        return super().changelist_view(request, extra_context=extra_context)


class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class InventoryAdmin(admin.ModelAdmin):
    inlines = [InventoryItemInline]
    list_display = ('get_inventory_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')
    list_per_page = 25

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


class WriteOffItemInline(admin.TabularInline):
    model = WriteOffItem
    extra = 1
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


class WriteOffAdmin(admin.ModelAdmin):
    inlines = [WriteOffItemInline]
    list_display = ('get_write_off_items', 'id', 'created_at', 'calculate_total_quantity', 'calculate_total_amount')
    readonly_fields = ('calculate_total_quantity', 'calculate_total_amount')
    list_per_page = 25

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


class BlogPostAdmin(TranslationAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'created_at')
    readonly_fields = ('created_at',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    list_display = ('name',)


@admin.register(Size)
class SizeAdmin(TranslationAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'description')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price', 'thumbnail_image_modification', 'get_stock')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'email', 'created_at', 'status')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'phone', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]

    fieldsets = (
        ('Статус', {
            'fields': ('status',)
        }),
        ('Персональные данные', {
            'fields': ('name', 'surname', 'phone', 'email', 'contact_method')
        }),
        ('Информация о доставке', {
            'fields': ('delivery_method', 'city', 'post_office')
        }),
        ('Информация об оплате', {
            'fields': ('payment_method',)
        }),
        ('Дополнительная информация', {
            'fields': ('comment',)
        }),
        ('Дата создания', {
            'fields': ('created_at',)
        }),
    )

    ordering = ('-created_at',)


class PreOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'text', 'drop', 'receipt_issued', 'ttn', 'shipped_to_customer', 'status', 'created_at',
        'updated_at',)
    list_display_links = ('id', 'full_name')
    list_filter = ('shipped_to_customer', 'receipt_issued', 'drop',)
    search_fields = ('full_name', 'text', 'ttn')
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.save(request=request)
        super().save_model(request, obj, form, change)


admin.site.register(ReturnItem, ReturnItemAdmin)
admin.site.register(PreOrder, PreOrderAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(WriteOff, WriteOffAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ProductModification, ProductModificationAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Return, ReturnAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
