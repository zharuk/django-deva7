from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template import loader
from django.utils.translation import get_language
from django.views import View
import json

from catalog.forms import OrderForm
from catalog.models import Image, Category, Product, BlogPost, ProductModification, Order, OrderItem
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    # Определяем заголовок блога в зависимости от языка
    main_page_post = get_object_or_404(
        BlogPost,
        Q(title='Головна сторінка') | Q(title='Главная страница')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]

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


def contacts_page(request):
    contacts_page_post = get_object_or_404(
        BlogPost,
        Q(title='Контакти') | Q(title='Контакты')
    )

    # Получаем категории и сортируем их по количеству продуктов
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    # Отображаем страницу contacts_page.html, передавая категории и выбранный блог
    return render(request, 'contacts_page.html', {'categories': categories,
                                                  'contacts_page_post': contacts_page_post,
                                                  'cart_total_quantity': cart_total_quantity,
                                                  'cart_total_price': cart_total_price})


def delivery_payment_page(request):
    delivery_payment_page_post = get_object_or_404(
        BlogPost,
        Q(title='Доставка и оплата') | Q(title='Доставка і оплата')
    )
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    # Получение данных о корзине
    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'delivery_payment_page.html',
                  {'categories': categories,
                           'delivery_payment_page_post': delivery_payment_page_post,
                           'cart_total_quantity': cart_total_quantity,
                           'cart_total_price': cart_total_price})


def privacy_policy_page(request):
    privacy_policy_page_post = get_object_or_404(
        BlogPost,
        Q(title='Політика конфіденційності') | Q(title='Политика конфиденциальности')
    )

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
    quantity = int(request.POST.get('quantity', 1))  # Получаем количество товара из формы

    if modification.stock >= quantity > 0:  # Проверяем, что количество товара доступно на складе и больше 0
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']
        cart[custom_sku] = cart.get(custom_sku, 0) + quantity  # Добавляем указанное количество товара в корзину
        request.session.modified = True

    return redirect('cart_view')


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_view')


def remove_from_cart(request, custom_sku):
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
        item_total_regular = modification.product.retail_price * quantity
        item_total_sale = modification.product.retail_sale_price * quantity if modification.product.retail_sale_price > 0 else 0
        cart_total_price += item_total_sale if item_total_sale > 0 else item_total_regular
        cart_total_quantity += quantity
        cart_items.append({'modification': modification,
                           'quantity': quantity,
                           'item_total_regular': item_total_regular,
                           'item_total_sale': item_total_sale})

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    cart_items_json = json.dumps([{'modification': {'custom_sku': item['modification'].custom_sku}, 'quantity': item['quantity']} for item in cart_items])

    return render(request, 'cart.html',
                  {'categories': categories, 'cart_items': cart_items, 'cart_total_price': cart_total_price,
                   'cart_total_quantity': cart_total_quantity, 'cart_items_json': cart_items_json})


def get_cart_info(request):
    cart = request.session.get('cart', {})
    custom_skus = cart.keys()
    modifications = ProductModification.objects.filter(custom_sku__in=custom_skus)

    cart_total_price = sum(
        modification.product.retail_sale_price * cart[modification.custom_sku]
        if modification.product.retail_sale_price > 0
        else modification.product.retail_price * cart[modification.custom_sku]
        for modification in modifications
    )
    cart_total_quantity = sum(cart.values())

    return cart_total_quantity, cart_total_price


@transaction.atomic
def complete_order(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    # Получаем корзину из сессии и информацию о товарах
    cart = request.session.get('cart', {})
    custom_skus = cart.keys()
    modifications = ProductModification.objects.filter(custom_sku__in=custom_skus)

    # Формируем данные о товарах в корзине для передачи в шаблон
    cart_items = []
    cart_total_price = 0
    cart_total_quantity = 0

    for modification in modifications:
        quantity = cart[modification.custom_sku]
        item_total_regular = modification.product.retail_price * quantity
        item_total_sale = modification.product.retail_sale_price * quantity if modification.product.retail_sale_price > 0 else 0
        cart_total_price += item_total_sale if item_total_sale > 0 else item_total_regular
        cart_total_quantity += quantity
        cart_items.append({'modification': modification,
                           'quantity': quantity,
                           'item_total_regular': item_total_regular,
                           'item_total_sale': item_total_sale})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем объект заказа
            order = Order(
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                contact_method=', '.join(form.cleaned_data['contact_method']),
                delivery_method=dict(form.fields['delivery_method'].choices)[form.cleaned_data['delivery_method']],
                city=form.cleaned_data['city'],
                post_office=form.cleaned_data['post_office'],
                payment_method=dict(form.fields['payment_method'].choices)[form.cleaned_data['payment_method']],
                comment=form.cleaned_data['comment'],
                status='pending',
            )
            order.save()
            request.session['last_order_id'] = order.id

            # Создаем объекты OrderItem для каждого товара в корзине и связываем их с заказом
            for modification in modifications:
                quantity = cart.get(str(modification.custom_sku), 0)
                if quantity > 0:
                    order_item = OrderItem.objects.create(
                        order=order,
                        product_modification=modification,
                        quantity=quantity
                    )

            # Очищаем корзину после оформления заказа
            del request.session['cart']

            # Редирект на страницу благодарности
            return redirect('thank_you_page')  # Замените 'thank_you_page' на ваше имя URL-адреса

    else:
        form = OrderForm()

    return render(request, 'complete_order.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total_price': cart_total_price,
        'cart_total_quantity': cart_total_quantity,
        'categories': categories
    })


def thank_you_page(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    # Получаем идентификатор последнего оформленного заказа из сессии
    last_order_id = request.session.get('last_order_id')

    # Получаем последний оформленный заказ по его идентификатору
    last_order = None
    if last_order_id is not None:
        last_order = Order.objects.get(id=last_order_id)

    # Вызываем методы calculate_total_amount и calculate_total_retail_amount
    total_amount = last_order.calculate_total_retail_amount()

    return render(request, 'thank_you_page.html', {
        'order': last_order,
        'total_amount': total_amount,
        'categories': categories,
    })
