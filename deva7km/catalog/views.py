import logging
from functools import wraps
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from catalog.models import Image, Category, Product, BlogPost, TelegramUser
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.generate_xlsx import generate_product_xlsx
from django.contrib import messages
from django.utils import timezone, translation
from datetime import timedelta
from .management.commands.update_tracking_status import update_tracking_status
from .models import PreOrder
from asgiref.sync import sync_to_async
import asyncio

# Настройка логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Убедитесь, что уровень логгирования соответствует вашим требованиям
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def home(request):
    main_page_post = get_object_or_404(
        BlogPost,
        Q(title='Головна сторінка') | Q(title='Главная страница')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]


    return render(request, 'home.html',
                  {'categories': categories, 'latest_products': latest_products, 'main_page_post': main_page_post,})


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

    context = {'category': category, 'products': products, 'categories': categories,}
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

    return render(request, 'product_detail.html',
                  {'product': product, 'categories': categories, 'unique_color_images': unique_color_images,
                   'modifications': modifications, 'product_url': product_url,})


def sales(request):
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')
    sale_products = Product.objects.filter(is_sale=True, is_active=True).order_by('-created_at')

    return render(request, 'sales.html',
                  {'sale_products': sale_products, 'categories': categories,})


def contacts_page(request):
    contacts_page_post = get_object_or_404(
        BlogPost,
        Q(title='Контакти') | Q(title='Контакты')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    return render(request, 'contacts_page.html', {'categories': categories, 'contacts_page_post': contacts_page_post,})


def delivery_payment_page(request):
    delivery_payment_page_post = get_object_or_404(
        BlogPost,
        Q(title='Доставка и оплата') | Q(title='Доставка і оплата')
    )
    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    return render(request, 'delivery_payment_page.html',
                  {'categories': categories, 'delivery_payment_page_post': delivery_payment_page_post,})


def privacy_policy_page(request):
    privacy_policy_page_post = get_object_or_404(
        BlogPost,
        Q(title='Політика конфіденційності') | Q(title='Политика конфиденциальности')
    )

    categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')

    return render(request, 'privacy_policy_page.html',
                  {'categories': categories, 'privacy_policy_page_post': privacy_policy_page_post,})


def telegram_page(request):
    return render(request, 'telegram_page.html')


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


async def update_tracking_status_view(request):
    try:
        ten_days_ago = timezone.now() - timedelta(days=10)
        recent_preorders = await sync_to_async(list)(PreOrder.objects.filter(created_at__gte=ten_days_ago))
        tasks = [update_tracking_status(preorder) for preorder in recent_preorders]
        await asyncio.gather(*tasks)
        await sync_to_async(messages.success)(request,
                                              "Статусы всех заказов, созданных за последние 10 дней, успешно обновлены.")
        logger.info("Статусы всех заказов, созданных за последние 10 дней, успешно обновлены.")
    except Exception as e:
        logger.error(f"Произошла ошибка при обновлении статусов: {e}")
        await sync_to_async(messages.error)(request, "Произошла ошибка при обновлении статусов.")
    return await sync_to_async(redirect)('admin:catalog_preorder_changelist')


def check_telegram_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        telegram_id = request.GET.get('telegram_id')
        current_path = request.GET.get('next', request.get_full_path())
        logger.debug(f"Extracted telegram_id: {telegram_id}")
        logger.debug(f"Current path: {current_path}")
        logger.debug(f"Request user: {request.user}")

        if request.user.is_authenticated:
            try:
                telegram_user = getattr(request.user, 'telegram_user', None)
                if telegram_user:
                    logger.debug(f"Found associated TelegramUser: {telegram_user}")
                    if telegram_user.role in ['admin', 'seller']:
                        logger.debug(f"User role ({telegram_user.role}) allows access.")
                        request.telegram_user = telegram_user
                        return view_func(request, *args, **kwargs)
                    else:
                        logger.debug(f"User role ({telegram_user.role}) does not allow access.")
                        return HttpResponseForbidden("У вас недостаточно прав для доступа к этой странице.")
                else:
                    logger.debug("No associated TelegramUser found.")
                    return HttpResponseForbidden("У вас нет связанного аккаунта Telegram.")
            except AttributeError as e:
                logger.error(f"AttributeError: {str(e)}")
                return HttpResponseForbidden("У вас нет связанного аккаунта Telegram.")

        if not request.user.is_authenticated:
            if telegram_id:
                logger.debug("Processing with telegram_id for unauthenticated user.")
                try:
                    telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                    logger.debug(f"Found TelegramUser: {telegram_user}")

                    if telegram_user.role in ['admin', 'seller']:
                        logger.debug(f"User role ({telegram_user.role}) allows access.")
                        if telegram_user.user:
                            django_login(request, telegram_user.user, backend='django.contrib.auth.backends.ModelBackend')
                            logger.debug(f"User {telegram_user.user} logged in.")
                            redirect_url = request.GET.get('next', request.path)
                            logger.debug(f"Redirecting to: {redirect_url}")
                            return redirect(redirect_url)
                        else:
                            logger.debug("No Django user associated with the TelegramUser.")
                            return HttpResponseForbidden("У вас нет связанного аккаунта Telegram.")
                    else:
                        logger.debug(f"User role ({telegram_user.role}) does not allow access.")
                        return redirect('login')
                except TelegramUser.DoesNotExist:
                    logger.debug("TelegramUser does not exist.")
                    return HttpResponseForbidden("У вас нет связанного аккаунта Telegram.")
            else:
                logger.debug("User not authenticated and no telegram_id provided. Redirecting to login.")
                return redirect(f"{reverse('login')}?next={current_path}")

    return _wrapped_view


@check_telegram_user
def seller_cabinet_main(request):
    return render(request, 'seller_cabinet/main.html')


@check_telegram_user
def seller_cabinet_sales(request):
    return render(request, 'seller_cabinet/sales/seller_sales.html')


@check_telegram_user
def seller_cabinet_returns(request):
    return render(request, 'seller_cabinet/returns/seller_returns.html')


@check_telegram_user
def seller_cabinet_inventory(request):
    return render(request, 'seller_cabinet/inventory/seller_inventory.html')


@check_telegram_user
def seller_cabinet_write_off(request):
    return render(request, 'seller_cabinet/write_off/seller_write_off.html')


@check_telegram_user
def preorders(request):
    return render(request, 'seller_cabinet/preorders/seller_preorders.html', {'user_id': request.user.id})


@csrf_exempt
@check_telegram_user
def seller_cabinet_reports(request):
    return render(request, 'seller_cabinet/reports/seller_reports.html')


def xml_generator_page(request):
    """
    Отображает страницу с формой для генерации XML-фида.
    """
    return render(request, 'xml_generator_page.html')


def generate_custom_feed(request):
    """
    Генерирует XML-фид на лету на основе GET-параметров.
    Параметры:
    - feed_type: 'rozetka' или 'facebook'
    - markup_type: 'percent' или 'fixed'
    - markup: целочисленное значение наценки
    - lang: 'uk' или 'ru'
    """
    # 1. Получаем и валидируем параметры (без изменений)
    feed_type = request.GET.get('feed_type', 'facebook')
    markup_type = request.GET.get('markup_type', 'percent')
    markup_str = request.GET.get('markup', '0')
    language = request.GET.get('lang', 'uk')

    if feed_type not in ['rozetka', 'facebook']:
        return HttpResponseBadRequest("Неверный тип фида. Доступные: 'rozetka', 'facebook'.")

    if markup_type not in ['percent', 'fixed']:
        return HttpResponseBadRequest("Неверный тип наценки. Доступные: 'percent', 'fixed'.")

    if language not in ['uk', 'ru']:
        return HttpResponseBadRequest("Неверный язык. Доступные: 'uk', 'ru'.")

    try:
        markup = int(markup_str)
        if markup < 0:
            markup = 0
    except (ValueError, TypeError):
        markup = 0

    # 2. Активируем нужный язык (без изменений)
    translation.activate(language)

    # 3. Получаем все активные товары (без изменений)
    products = Product.objects.filter(is_active=True).prefetch_related(
        'modifications__color', 'modifications__size', 'category'
    )

    # 4. ЛОГИКА ПРИМЕНЕНИЯ НАЦЕНКИ (теперь применяется только к оптовым ценам)
    if markup > 0:
        if markup_type == 'percent':
            markup_multiplier = 1 + (markup / 100.0)
            for product in products:
                product.price = int(product.price * markup_multiplier)
                if product.sale_price > 0:
                    product.sale_price = int(product.sale_price * markup_multiplier)

        elif markup_type == 'fixed':
            for product in products:
                product.price += markup
                if product.sale_price > 0:
                    product.sale_price += markup

    # 5. ОБНОВЛЕННЫЙ ВЫБОР ШАБЛОНА
    if feed_type == 'rozetka':
        template_name = 'rozetka_feed_generator.xml'  # <-- ИСПОЛЬЗУЕМ НОВЫЙ ШАБЛОН
        categories = Category.objects.all()
        context = {'products': products, 'categories': categories}
        content_type = 'application/xml; charset=utf-8'
    else:  # По умолчанию Facebook
        template_name = 'fb_feed_generator.xml'  # <-- ИСПОЛЬЗУЕМ НОВЫЙ ШАБЛОН
        context = {
            'products': products,
            'language': language,
            'request': request
        }
        content_type = 'text/xml; charset=utf-8'

    # 6. Рендерим XML и возвращаем ответ (без изменений)
    xml_content = render_to_string(template_name, context)
    return HttpResponse(xml_content, content_type=content_type)