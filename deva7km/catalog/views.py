from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from catalog.models import Image, Category, Product


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.product_set.all()
    categories = Category.objects.all()  # Добавлено получение всех категорий для формирования меню
    return render(request, 'category_detail.html',
                  {'category': category, 'products': products, 'categories': categories})


def product_list(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'product_list.html', {'category': category, 'products': products})


def product_detail(request, category_slug, product_slug):
    category = Category.objects.get(slug=category_slug)
    product = Product.objects.get(slug=product_slug, category=category)

    # Получение уникальных цветов для данного товара
    unique_colors = product.modifications.values('color__name').annotate(count=Count('color')).filter(count__gt=0)

    # Формирование словаря с уникальными цветами и изображениями
    unique_color_images = {}
    for color in unique_colors:
        modification = product.modifications.filter(color__name=color['color__name']).first()
        if modification:
            images = Image.objects.filter(modification=modification)
            unique_color_images[color['color__name']] = images

    # Получение всех категорий (или нужные данные для формирования меню)
    categories = Category.objects.all()

    return render(request, 'product_detail.html', {'product': product, 'categories': categories,
                                                   'unique_color_images': unique_color_images})
