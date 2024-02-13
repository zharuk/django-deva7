from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils.translation import get_language
from django.views import View
from transliterate.utils import _

from catalog.models import Image, Category, Product, BlogPost, ProductModification, Sale, SaleItem
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    language = get_language()
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    if language == 'uk':
        main_page_post = get_object_or_404(BlogPost, title=_(u'Головна сторінка'))
    else:
        main_page_post = get_object_or_404(BlogPost, title=_(u'Главная страница'))

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'home.html',
                  {'categories': categories, 'latest_products': latest_products, 'main_page_post': main_page_post,
                   'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products_list = category.product_set.filter(is_active=True).order_by('-created_at')
    items_per_page = 9
    paginator = Paginator(products_list, items_per_page)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    context = {'category': category, 'products': products, 'categories': categories,
               'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price}
    return render(request, 'category_detail.html', context)


def product_detail(request, category_slug, product_slug):
    # Получение категории или возврат ошибки 404, если категория не найдена
    category = get_object_or_404(Category, slug=category_slug)

    # Получение товара или возврат ошибки 404, если товар не найден
    product = get_object_or_404(Product, slug=product_slug, category=category)

    # Получение абсолютного URL продукта
    product_url = request.build_absolute_uri()

    # Получение всех модификаций товара и сортировка их по цвету, а затем по размеру
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

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'product_detail.html', {'product': product, 'categories': categories,
                                                   'unique_color_images': unique_color_images,
                                                   'modifications': modifications,
                                                   'product_url': product_url,
                                                   'cart_total_quantity': cart_total_quantity,
                                                   'cart_total_price': cart_total_price})


def sales(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    sale_products = Product.objects.filter(is_sale=True, is_active=True).order_by('-created_at')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'sales.html', {'sale_products': sale_products, 'categories': categories,
                                          'cart_total_quantity': cart_total_quantity,
                                          'cart_total_price': cart_total_price})


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

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    # Отображаем страницу about_page.html, передавая категории, выбранный блог и данные о корзине
    return render(request, 'about_page.html', {'categories': categories, 'about_page_post': about_page_post,
                                               'cart_total_quantity': cart_total_quantity,
                                               'cart_total_price': cart_total_price})


def contacts_page(request):
    # Получаем текущий язык запроса
    current_language = request.LANGUAGE_CODE

    # Определяем соответствующий заголовок блога в зависимости от языка
    if current_language == 'uk':
        # Если текущий язык украинский, выбираем блог с заголовком "Контакти"
        contact_page_post = get_object_or_404(BlogPost, title=_('Контакти'))
    else:
        # Иначе (если текущий язык не украинский), выбираем блог с заголовком "Контакты"
        contact_page_post = get_object_or_404(BlogPost, title=_('Контакты'))

    # Получаем категории и сортируем их по количеству продуктов
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    # Отображаем страницу contacts_page.html, передавая категории и выбранный блог
    return render(request, 'contacts_page.html', {'categories': categories, 'contact_page_post': contact_page_post,
                                                  'cart_total_quantity': cart_total_quantity,
                                                  'cart_total_price': cart_total_price})


def delivery_page(request):
    delivery_page_post = get_object_or_404(BlogPost, title='Доставка')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'delivery_page.html', {'categories': categories, 'delivery_page_post': delivery_page_post,
                                                  'cart_total_quantity': cart_total_quantity,
                                                  'cart_total_price': cart_total_price})


def payment_page(request):
    payment_page_post = get_object_or_404(BlogPost, title='Оплата')
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'payment_page.html', {'categories': categories, 'payment_page_post': payment_page_post,
                                                 'cart_total_quantity': cart_total_quantity,
                                                 'cart_total_price': cart_total_price})


def privacy_policy_page(request):
    # Получаем текущий язык запроса
    current_language = request.LANGUAGE_CODE

    # Определяем соответствующий заголовок блога в зависимости от языка
    if current_language == 'uk':
        # Если текущий язык украинский, выбираем блог с заголовком "Політика конфіденційності"
        privacy_policy_page_post = get_object_or_404(BlogPost, title=_('Політика конфіденційності'))
    else:
        # Иначе (если текущий язык не украинский), выбираем блог с заголовком "Политика конфиденциальности"
        privacy_policy_page_post = get_object_or_404(BlogPost, title=_('Политика конфиденциальности'))

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'privacy_policy_page.html',
                  {'categories': categories, 'privacy_policy_page_post': privacy_policy_page_post,
                   'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price})


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


def add_to_cart(request, custom_sku):
    modification = get_object_or_404(ProductModification, custom_sku=custom_sku)

    if modification.stock > 0:
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']
        cart[custom_sku] = cart.get(custom_sku, 0) + 1
        request.session.modified = True

    return redirect('cart_view')


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_view')


def remove_from_cart(request, custom_sku):
    print(custom_sku)
    if 'cart' in request.session:
        cart = request.session['cart']
        if custom_sku in cart:
            del cart[custom_sku]
            request.session.modified = True
    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    custom_skus = cart.keys()
    modifications = ProductModification.objects.filter(custom_sku__in=custom_skus)

    cart_items = []
    cart_total_price = 0
    cart_total_quantity = 0

    for modification in modifications:
        quantity = cart[modification.custom_sku]
        item_total = modification.price * quantity
        cart_total_price += item_total
        cart_total_quantity += quantity
        cart_items.append({'modification': modification, 'quantity': quantity, 'item_total': item_total})

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    return render(request, 'cart.html',
                  {'categories': categories, 'cart_items': cart_items, 'cart_total_price': cart_total_price,
                   'cart_total_quantity': cart_total_quantity})


def complete_order(request):
    # Логика обработки данных формы и создания заказа
    if request.method == 'POST':
        # Обработка данных формы и создание заказа
        pass  # Замените этот плейсхолдер на вашу реальную логику создания заказа

    # Получаем информацию о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    # Получаем список товаров, которые заказываются
    cart = request.session.get('cart', {})
    custom_skus = cart.keys()
    modifications = ProductModification.objects.filter(custom_sku__in=custom_skus)

    ordered_items = []
    ordered_items_total_price = 0  # Общая сумма всех заказанных товаров

    for modification in modifications:
        quantity = cart[modification.custom_sku]
        item_total = modification.price * quantity
        ordered_items_total_price += item_total
        ordered_items.append({'modification': modification, 'quantity': quantity, 'item_total': item_total})

    # Отображение страницы оформления заказа
    return render(request, 'complete_order.html', context={'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price, 'ordered_items': ordered_items, 'ordered_items_total_price': ordered_items_total_price})


def get_cart_info(request):
    cart = request.session.get('cart', {})
    custom_skus = cart.keys()
    modifications = ProductModification.objects.filter(custom_sku__in=custom_skus)

    cart_total_price = sum(modification.price * cart[modification.custom_sku] for modification in modifications)
    cart_total_quantity = sum(cart.values())

    return cart_total_quantity, cart_total_price
