from django.db.models import Count
from django.http import Http404, HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from catalog.models import Image, Category, Product, BlogPost, ProductModification
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    main_page_post = get_object_or_404(BlogPost, title='Главная страница')
    return render(request, 'home.html',
                  {'categories': categories, 'latest_products': latest_products, 'main_page_post': main_page_post})


def category_detail(request, category_slug):
    # Получение объекта категории по slug
    category = get_object_or_404(Category, slug=category_slug)

    # Получение всех товаров в данной категории и упорядочивание их по полю title
    products_list = category.product_set.filter(is_active=True).order_by('-created_at')

    # Количество товаров, которое вы хотите отобразить на каждой странице
    items_per_page = 9

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

    # Получение всех категорий для формирования меню
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Передача данных в контекст для использования в шаблоне
    context = {'category': category, 'products': products, 'categories': categories}

    # Возвращение ответа с использованием шаблона 'category_detail.html' и передачей контекста
    return render(request, 'category_detail.html', context)


def product_detail(request, category_slug, product_slug):
    # Изменение здесь: использование get_object_or_404 для категории
    category = get_object_or_404(Category, slug=category_slug)

    # Изменение здесь: использование filter вместо get для поиска товара
    product = Product.objects.filter(slug=product_slug, category=category).first()

    if not product:
        # Если товар не найден, возвращаем 404
        raise Http404("Product not found")

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
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    return render(request, 'product_detail.html', {'product': product, 'categories': categories,
                                                   'unique_color_images': unique_color_images})


def sales(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    sale_products = Product.objects.filter(is_sale=True, is_active=True).order_by('-created_at')
    return render(request, 'sales.html', {'sale_products': sale_products, 'categories': categories})


def all_products(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'all_products.html', {'products': products, 'categories': categories})


def about_page(request):
    about_page_post = get_object_or_404(BlogPost, title='О сайте')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'about_page.html', {'categories': categories, 'about_page_post': about_page_post})


def contacts_page(request):
    contacts_page_post = get_object_or_404(BlogPost, title='Контакты')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'contacts_page.html', {'categories': categories, 'contacts_page_post': contacts_page_post})


def delivery_page(request):
    delivery_page_post = get_object_or_404(BlogPost, title='Доставка')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'delivery_page.html', {'categories': categories, 'delivery_page_post': delivery_page_post})


def payment_page(request):
    payment_page_post = get_object_or_404(BlogPost, title='Оплата')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'payment_page.html', {'categories': categories, 'payment_page_post': payment_page_post})


def telegram_page(request):
    return render(request, 'telegram_page.html')


class FacebookFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        context = {'products': products, 'modifications': modifications, 'images': images, 'request': request}
        template = loader.get_template('fb_feed.xml')
        xml_content = template.render(context)
        response = HttpResponse(xml_content, content_type='application/xml')
        return response
