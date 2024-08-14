import json
import re

from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import get_language
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from catalog.email_utils import send_new_order_notification_email
from catalog.forms import PreOrderForm
from catalog.models import Image, Category, Product, BlogPost, ProductModification, Order, OrderItem, Sale, SaleItem, \
    Return, Inventory, WriteOff
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.generate_xlsx import generate_product_xlsx
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .management.commands.update_tracking_status import update_tracking_status
from .models import PreOrder
from asgiref.sync import sync_to_async, async_to_sync
import asyncio

from .services import handle_preorder_form, toggle_preorder_status
from .utils import notify_preorder_change


def home(request):
    main_page_post = get_object_or_404(
        BlogPost,
        Q(title='Головна сторінка') | Q(title='Главная страница')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]

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

    cart_total_quantity, cart_total_price = get_cart_info(request)

    context = {'category': category, 'products': products, 'categories': categories,
               'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price}
    return render(request, 'category_detail.html', context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)

    product_url = request.build_absolute_uri()
    modifications = product.modifications.all().order_by('color__name', 'size__name')

    current_language = get_language()
    unique_colors = modifications.values('color__name', f'color__name_{current_language}').annotate(
        count=Count('color')).filter(count__gt=0)

    unique_color_images = {}
    for color in unique_colors:
        color_name = color[f'color__name_{current_language}']
        modification = modifications.filter(color__name=color['color__name']).first()
        if modification:
            images = Image.objects.filter(modification=modification)
            unique_color_images[color_name] = images

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'product_detail.html',
                  {'product': product, 'categories': categories, 'unique_color_images': unique_color_images,
                   'modifications': modifications, 'product_url': product_url,
                   'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price})


def sales(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    sale_products = Product.objects.filter(is_sale=True, is_active=True).order_by('-created_at')

    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'sales.html',
                  {'sale_products': sale_products, 'categories': categories, 'cart_total_quantity': cart_total_quantity,
                   'cart_total_price': cart_total_price})


def contacts_page(request):
    contacts_page_post = get_object_or_404(
        BlogPost,
        Q(title='Контакти') | Q(title='Контакты')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'contacts_page.html', {'categories': categories, 'contacts_page_post': contacts_page_post,
                                                  'cart_total_quantity': cart_total_quantity,
                                                  'cart_total_price': cart_total_price})


def delivery_payment_page(request):
    delivery_payment_page_post = get_object_or_404(
        BlogPost,
        Q(title='Доставка и оплата') | Q(title='Доставка і оплата')
    )
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'delivery_payment_page.html',
                  {'categories': categories, 'delivery_payment_page_post': delivery_payment_page_post,
                   'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price})


def privacy_policy_page(request):
    privacy_policy_page_post = get_object_or_404(
        BlogPost,
        Q(title='Політика конфіденційності') | Q(title='Политика конфиденциальности')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    cart_total_quantity, cart_total_price = get_cart_info(request)

    return render(request, 'privacy_policy_page.html',
                  {'categories': categories, 'privacy_policy_page_post': privacy_policy_page_post,
                   'cart_total_quantity': cart_total_quantity, 'cart_total_price': cart_total_price})


def telegram_page(request):
    return render(request, 'telegram_page.html')


def add_to_cart(request, custom_sku):
    modification = get_object_or_404(ProductModification, custom_sku=custom_sku)
    quantity = int(request.POST.get('quantity', 1))

    if modification.stock >= quantity > 0:
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']
        cart[custom_sku] = cart.get(custom_sku, 0) + quantity
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
        cart_items.append({'modification': modification, 'quantity': quantity, 'item_total_regular': item_total_regular,
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
        cart_items.append({'modification': modification, 'quantity': quantity, 'item_total_regular': item_total_regular,
                           'item_total_sale': item_total_sale})

    if request.method == 'POST':
        form = PreOrderForm(request.POST)
        if form.is_valid():
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

            for modification in modifications:
                quantity = cart.get(str(modification.custom_sku), 0)
                if quantity > 0:
                    OrderItem.objects.create(order=order, product_modification=modification, quantity=quantity)

            send_new_order_notification_email(order, cart_items, cart_total_price, cart_total_quantity)
            del request.session['cart']
            return redirect('thank_you_page')

    else:
        form = PreOrderForm()

    return render(request, 'complete_order.html',
                  {'form': form, 'cart_items': cart_items, 'cart_total_price': cart_total_price,
                   'cart_total_quantity': cart_total_quantity, 'categories': categories})


def thank_you_page(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    last_order_id = request.session.get('last_order_id')

    last_order = None
    if last_order_id is not None:
        last_order = Order.objects.get(id=last_order_id)

    total_amount = last_order.calculate_total_retail_amount()

    return render(request, 'thank_you_page.html',
                  {'order': last_order, 'total_amount': total_amount, 'categories': categories})


def product_search(request):
    query = request.GET.get('query', '').strip()

    results = []
    if query:
        results = Product.objects.filter(Q(title__icontains=query) | Q(sku__icontains=query)).order_by('title')
        results = [product for product in results if product.get_total_stock() > 0]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [{'title': product.title, 'get_absolute_url': product.get_absolute_url(),
                 'collage_image_url': product.collage_image.url if product.collage_image else '/static/images/default_image.png'}
                for product in results[:10]]
        return JsonResponse(data, safe=False)

    return render(request, 'product_search.html', {'results': results, 'query': query})


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


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def export_products_xlsx(request):
    response = generate_product_xlsx(request)
    return response


import logging

logger_tracking = logging.getLogger('tracking')


async def update_tracking_status_view(request):
    try:
        ten_days_ago = timezone.now() - timedelta(days=10)
        recent_preorders = await sync_to_async(list)(PreOrder.objects.filter(created_at__gte=ten_days_ago))
        tasks = [update_tracking_status(preorder) for preorder in recent_preorders]
        await asyncio.gather(*tasks)
        await sync_to_async(messages.success)(request,
                                              "Статусы всех заказов, созданных за последние 10 дней, успешно обновлены.")
    except Exception as e:
        logger_tracking.error(f"Произошла ошибка при обновлении статусов: {e}")
        await sync_to_async(messages.error)(request, "Произошла ошибка при обновлении статусов.")
    return await sync_to_async(redirect)('admin:catalog_preorder_changelist')


@login_required
def seller_cabinet_main(request):
    return render(request, 'seller_cabinet/main.html')


@login_required
def seller_cabinet_sales(request):
    return render(request, 'seller_cabinet/sales/seller_sales.html')


@login_required
def seller_cabinet_returns(request):
    return render(request, 'seller_cabinet/returns/seller_returns.html')


@login_required
def seller_cabinet_inventory(request):
    return render(request, 'seller_cabinet/inventory/seller_inventory.html')


@login_required
def seller_cabinet_write_off(request):
    return render(request, 'seller_cabinet/write_off/seller_write_off.html')


@login_required
def preorders(request):
    return render(request, 'seller_cabinet/preorders/seller_preorders.html', {'user_id': request.user.id})
