from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from catalog.email_utils import send_new_order_notification_email
from catalog.forms import OrderForm
from catalog.models import Image, Category, Product, BlogPost, ProductModification, Order, OrderItem, Sale, SaleItem
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.generate_xlsx import generate_product_xlsx
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .management.commands.update_tracking_status import update_tracking_status
from .models import PreOrder
from asgiref.sync import sync_to_async
import asyncio


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

    return render(request, 'cart.html',
                  {'categories': categories, 'cart_items': cart_items, 'cart_total_price': cart_total_price,
                   'cart_total_quantity': cart_total_quantity})


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
                    OrderItem.objects.create(
                        order=order,
                        product_modification=modification,
                        quantity=quantity
                    )

            # Отправка уведомления о новом заказе администратору
            send_new_order_notification_email(order, cart_items, cart_total_price, cart_total_quantity)

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


# Функция для обычного поиска
def product_search(request):
    query = request.GET.get('query', '').strip()  # Оставляем запрос как есть, без приведения к нижнему регистру

    results = []
    if query:
        # Фильтрация по названию или артикулу, и проверка на остаток товара
        results = Product.objects.filter(
            Q(title__icontains=query) | Q(sku__icontains=query)
        ).order_by('title')  # Фильтрация по строке запроса и сортировка по названию

        # Применение фильтрации по остатку через Python, так как Django ORM не позволяет это сделать напрямую
        results = [product for product in results if product.get_total_stock() > 0]

    # Ограничение вывода результатов в AJAX-запросах
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'title': product.title,
                'get_absolute_url': product.get_absolute_url(),
                'collage_image_url': product.collage_image.url if product.collage_image else '/static/images/default_image.png'
            }
            for product in results[:10]  # Ограничение до 10 результатов
        ]
        return JsonResponse(data, safe=False)

    return render(request, 'product_search.html', {'results': results, 'query': query})


# Класс для AJAX поиска
class AjaxProductSearch(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()  # Оставляем запрос как есть, без приведения к нижнему регистру

        results = []
        if query:
            # Фильтрация по названию или артикулу, и проверка на остаток товара
            results = Product.objects.filter(
                Q(title__icontains=query) | Q(sku__icontains=query)
            ).order_by('title')  # Фильтрация по строке запроса и сортировка по названию

            # Применение фильтрации по остатку через Python, так как Django ORM не позволяет это сделать напрямую
            results = [product for product in results if product.get_total_stock() > 0]

            # Ограничение до 10 результатов
            results = results[:10]

        data = [
            {
                'title': product.title,
                'get_absolute_url': product.get_absolute_url(),
                'collage_image_url': product.collage_image.url if product.collage_image else '/static/images/default_image.png'
            }
            for product in results
        ]
        return JsonResponse(data, safe=False)


# профиль пользователя
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


# логин пользователя
@login_required
def profile_view(request):
    return render(request, 'profile.html')


# генерация товаров для checkbox
def export_products_xlsx(request):
    # Вызываем функцию для генерации XLSX
    response = generate_product_xlsx(request)
    return response


import logging

# Настройка логирования
logger_tracking = logging.getLogger('tracking')


async def update_tracking_status_view(request):
    try:
        ten_days_ago = timezone.now() - timedelta(days=10)

        # Асинхронное получение всех предзаказов за последние 10 дней
        recent_preorders = await sync_to_async(list)(PreOrder.objects.filter(created_at__gte=ten_days_ago))

        # Запускаем обновление статусов для всех найденных предзаказов
        tasks = [update_tracking_status(preorder) for preorder in recent_preorders]
        await asyncio.gather(*tasks)

        # Уведомляем пользователя об успешном обновлении
        await sync_to_async(messages.success)(request,
                                              "Статусы всех заказов, созданных за последние 10 дней, успешно обновлены.")

    except Exception as e:
        # Логирование ошибки
        logger_tracking.error(f"Произошла ошибка при обновлении статусов: {e}")
        # Уведомление пользователя об ошибке
        await sync_to_async(messages.error)(request, "Произошла ошибка при обновлении статусов.")

    # Перенаправляем обратно на страницу списка предзаказов
    return await sync_to_async(redirect)('admin:catalog_preorder_changelist')


@login_required
def seller_cabinet_main(request):
    return render(request, 'seller_cabinet/main.html')

@login_required
def seller_cabinet_sales(request):
    pending_sale = Sale.objects.filter(user=request.user, status='pending').first()
    today = timezone.now().date()
    daily_sales = Sale.objects.filter(created_at__date=today, status='completed')
    total_daily_sales_amount = sum(sale.calculate_total_amount() for sale in daily_sales)

    return render(request, 'seller_cabinet/sales/seller_sales.html', {
        'pending_sale': pending_sale,
        'daily_sales': daily_sales,
        'total_daily_sales_amount': total_daily_sales_amount,
        'today': today,
    })

from django.core.paginator import Paginator

@login_required
def search_article(request):
    article = request.GET.get('article', '')
    page_number = int(request.GET.get('page', 1))
    if len(article) >= 3:
        modifications = ProductModification.objects.filter(custom_sku__icontains=article)
        paginator = Paginator(modifications, 5)  # 5 результатов на страницу
        page_obj = paginator.get_page(page_number)
        has_more = page_obj.has_next()
    else:
        page_obj = []
        has_more = False
    return render(request, 'seller_cabinet/sales/partials/available_items.html', {
        'modifications': page_obj,
        'has_more': has_more,
        'next_page_number': page_number + 1 if has_more else None
    })


@csrf_exempt
def remove_item_from_sale(request):
    item_id = request.POST.get('item_id')
    SaleItem.objects.get(id=item_id).delete()

    sale = Sale.objects.get(user=request.user, status='pending')
    items_html = render_to_string('seller_cabinet/sales/partials/selected_items.html', {'sale': sale})
    total_amount = sale.calculate_total_amount()
    return JsonResponse({'items_html': items_html, 'total_amount': total_amount})

@csrf_exempt
def add_item_to_sale(request):
    try:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        product_modification = get_object_or_404(ProductModification, id=item_id)

        if product_modification.stock <= 0:
            return JsonResponse({'error': 'Товар отсутствует на складе'}, status=400)

        sale, created = Sale.objects.get_or_create(
            user=request.user, status='pending',
            defaults={'source': 'site'}
        )
        SaleItem.objects.create(
            sale=sale, product_modification=product_modification, quantity=quantity
        )

        items_html = render_to_string('seller_cabinet/sales/partials/selected_items.html', {'sale': sale})
        total_amount = sale.calculate_total_amount()
        return JsonResponse({'items_html': items_html, 'total_amount': total_amount})

    except ProductModification.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def confirm_sale(request):
    try:
        sale = Sale.objects.get(user=request.user, status='pending')
        sale.status = 'completed'
        sale.save()
        return JsonResponse({'message': 'Продажа успешно завершена!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_pending_sale_items(request):
    sale_id = request.GET.get('sale_id')
    sale = Sale.objects.get(id=sale_id, user=request.user, status='pending')
    items_html = render_to_string('seller_cabinet/sales/partials/selected_items.html', {'sale': sale})
    total_amount = sale.calculate_total_amount()
    return JsonResponse({'items_html': items_html, 'total_amount': total_amount})

@csrf_exempt
@login_required
def clear_sale(request):
    sale = Sale.objects.get(user=request.user, status='pending')
    sale.items.all().delete()
    return JsonResponse({'message': 'Корзина очищена!'})

@login_required
def get_daily_sales(request):
    today = timezone.now().date()
    daily_sales = Sale.objects.filter(created_at__date=today, status='completed')
    total_daily_sales_amount = sum(sale.calculate_total_amount() for sale in daily_sales)

    sales_html = render_to_string('seller_cabinet/sales/partials/daily_sales_items.html', {
        'daily_sales': daily_sales,
    })

    return JsonResponse({
        'sales_html': sales_html,
        'total_amount': total_daily_sales_amount,
    })
