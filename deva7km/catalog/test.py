from catalog.models import Product
from django.db.models.functions import Lower
from django.db.models import Q

# Тестовый запрос
query = 'платье'.strip().lower()

# Выполняем аннотацию и фильтрацию
results = Product.objects.annotate(
    title_lower=Lower('title'),
    sku_lower=Lower('sku')
).filter(
    Q(title_lower__icontains=query) | Q(sku_lower__icontains=query)
)

# Печатаем результаты
for product in results:
    print(f"Результат: {product.title} (SKU: {product.sku})")