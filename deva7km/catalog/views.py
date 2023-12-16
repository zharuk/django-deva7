from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views import View
from catalog.models import Image, Category, Product


def home(request):
    categories = Category.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:6]
    return render(request, 'home.html', {'categories': categories, 'latest_products': latest_products})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products_list = category.product_set.all()

    # Количество товаров, которое ты хочешь отобразить на каждой странице
    items_per_page = 18

    # Создание объекта Paginator
    paginator = Paginator(products_list, items_per_page)

    # Получение номера текущей страницы из запроса GET
    page = request.GET.get('page')

    try:
        # Получение списка товаров для текущей страницы
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если 'page' не является целым числом, вывод первой страницы
        products = paginator.page(1)
    except EmptyPage:
        # Если 'page' больше, чем общее количество страниц, вывод последней страницы
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()  # Добавлено получение всех категорий для формирования меню

    context = {'category': category, 'products': products, 'categories': categories}
    return render(request, 'category_detail.html', context)


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


class AllProductsView(View):
    def get(self, request):
        # Логика для отображения всех товаров
        products = Product.objects.all()  # Пример, ты можешь адаптировать под свою модель
        categories = Category.objects.all()
        return render(request, 'all_products.html', {'products': products, 'categories': categories})


def about_page(request):
    categories = Category.objects.all()
    return render(request, 'about_page.html', {'categories': categories})


def contacts_page(request):
    categories = Category.objects.all()
    return render(request, 'contacts_page.html', {'categories': categories})


def delivery_page(request):
    categories = Category.objects.all()
    return render(request, 'delivery_page.html', {'categories': categories})


def payment_page(request):
    categories = Category.objects.all()
    return render(request, 'payment_page.html', {'categories': categories})
