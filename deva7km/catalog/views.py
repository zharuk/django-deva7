from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Image, ProductModification, Category, Product


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.product_set.all()
    return render(request, 'category_detail.html', {'category': category, 'products': products})


def product_list(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'product_list.html', {'category': category, 'products': products})


def product_detail(request, category_slug, product_slug):
    category = Category.objects.get(slug=category_slug)
    product = Product.objects.get(slug=product_slug, category=category)
    images = Image.objects.filter(modification__product=product)  # Получите изображения товара
    return render(request, 'product_detail.html', {'product': product, 'images': images})
