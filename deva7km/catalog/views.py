from django.core.cache import cache
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.translation import get_language, activate
from django.views import View
from transliterate.utils import _

from catalog.models import Image, Category, Product, BlogPost, ProductModification
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from deva7km import settings


def home(request):
    # Определяем текущий язык
    language = get_language()

    # Получаем объекты категорий
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получаем последние активные продукты
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]

    # Получаем объект BlogPost в зависимости от текущего языка
    if language == 'uk':
        main_page_post = get_object_or_404(BlogPost, title=_(u'Головна сторінка'))
    else:
        main_page_post = get_object_or_404(BlogPost, title=_(u'Главная страница'))

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

    # Изменение здесь: сортировка модификаций по цвету, а затем по размеру
    modifications = product.modifications.all().order_by('color__name', 'size__name')

    # Получение текущего языка
    current_language = get_language()

    # Получение уникальных цветов для данного товара с учетом текущего языка
    unique_colors = modifications.values('color__name', f'color__name_{current_language}').annotate(
        count=Count('color')).filter(count__gt=0)

    # Формирование словаря с уникальными цветами и изображениями
    unique_color_images = {}
    for color in unique_colors:
        color_name = color[f'color__name_{current_language}']
        modification = modifications.filter(color__name=color['color__name']).first()
        if modification:
            images = Image.objects.filter(modification=modification)
            unique_color_images[color_name] = images

    # Получение всех категорий (или нужные данные для формирования меню)
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    return render(request, 'product_detail.html', {'product': product, 'categories': categories,
                                                   'unique_color_images': unique_color_images,
                                                   'modifications': modifications})


def sales(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    sale_products = Product.objects.filter(is_sale=True, is_active=True).order_by('-created_at')
    return render(request, 'sales.html', {'sale_products': sale_products, 'categories': categories})


def all_products(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'all_products.html', {'products': products, 'categories': categories})


def about_page(request):
    # Получаем текущий язык запроса
    current_language = request.LANGUAGE_CODE

    # Определяем соответствующий заголовок блога в зависимости от языка
    if current_language == 'uk':
        # Если текущий язык украинский, выбираем блог с заголовком "Про сайт"
        about_page_post = get_object_or_404(BlogPost, title=_('Про сайт'))
    else:
        # Иначе (если текущий язык не украинский), выбираем блог с заголовком "О сайте"
        about_page_post = get_object_or_404(BlogPost, title=_('О сайте'))

    # Получаем категории и сортируем их по количеству продуктов
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Отображаем страницу about_page.html, передавая категории и выбранный блог
    return render(request, 'about_page.html', {'categories': categories, 'about_page_post': about_page_post})


def contacts_page(request):
    # Получаем текущий язык запроса
    current_language = request.LANGUAGE_CODE

    # Определяем соответствующий заголовок блога в зависимости от языка
    if current_language == 'uk':
        # Если текущий язык украинский, выбираем блог с заголовком "Про сайт"
        about_page_post = get_object_or_404(BlogPost, title=_('Контакти'))
    else:
        # Иначе (если текущий язык не украинский), выбираем блог с заголовком "О сайте"
        about_page_post = get_object_or_404(BlogPost, title=_('Контакты'))

    # Получаем категории и сортируем их по количеству продуктов
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Отображаем страницу about_page.html, передавая категории и выбранный блог
    return render(request, 'about_page.html', {'categories': categories, 'about_page_post': about_page_post})


def delivery_page(request):
    delivery_page_post = get_object_or_404(BlogPost, title='Доставка')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'delivery_page.html', {'categories': categories, 'delivery_page_post': delivery_page_post})


def payment_page(request):
    payment_page_post = get_object_or_404(BlogPost, title='Оплата')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'payment_page.html', {'categories': categories, 'payment_page_post': payment_page_post})


def privacy_policy_page(request):
    privacy_policy_page_post = get_object_or_404(BlogPost, title='Политика конфиденциальности')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'privacy_policy_page.html',
                  {'categories': categories, 'privacy_policy_page_post': privacy_policy_page_post})


def telegram_page(request):
    return render(request, 'telegram_page.html')


# Представления для формирования фида Facebook
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


# Представления для формирования фида Google
class GoogleFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        context = {'products': products, 'modifications': modifications, 'images': images, 'request': request}
        template = loader.get_template('google_feed.xml')
        xml_content = template.render(context)
        response = HttpResponse(xml_content, content_type='application/xml')
        return response


# Представления для формирования фида Rozetka
class RozetkaFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        categories = Category.objects.all()  # Получаем все категории
        context = {'products': products, 'modifications': modifications, 'images': images, 'categories': categories,
                   'request': request}
        template = loader.get_template('rozetka_feed.xml')
        xml_content = template.render(context)
        response = HttpResponse(xml_content, content_type='application/xml')
        return response


def set_user_language(request):
    """
    Устанавливает язык пользователя на основе его предпочтений в сессии.
    Если язык не был установлен, используется украинский язык по умолчанию.
    """
    # Проверяем, был ли установлен язык для этого пользователя
    if 'language' in request.session:
        language = request.session['language']
    else:
        # Если язык не был установлен, устанавливаем украинский язык по умолчанию
        language = 'uk'

    # Активируем выбранный язык
    activate(language)
