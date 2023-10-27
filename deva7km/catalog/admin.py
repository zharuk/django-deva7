from django.contrib import admin
from .models import Product, ProductModification, Category, Image, Color, Size


class ProductModificationInline(admin.TabularInline):  # Или используйте admin.StackedInline для другого вида отображения
    model = ProductModification
    extra = 0  # Количество пустых форм для добавления модификаций


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModificationInline]  # Добавляем встроенные модификации товара


admin.site.register(Product, ProductAdmin)
#admin.site.register(Product)
admin.site.register(ProductModification)
#.site.register(Category)
admin.site.register(Image)
#admin.site.register(Color)
#admin.site.register(Size)
