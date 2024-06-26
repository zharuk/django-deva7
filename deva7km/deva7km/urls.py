from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from catalog import views
from catalog.feed_views import FacebookFeedView, GoogleFeedView, RozetkaFeedView
from catalog.views import home, contacts_page, \
    category_detail, product_detail, sales, telegram_page, \
    privacy_policy_page, cart_view, clear_cart, remove_from_cart, thank_you_page, delivery_payment_page, product_search, \
    ProfileDetailView, update_tracking_status_view, AjaxProductSearch, get_pending_sale_items, clear_sale, \
    get_daily_sales

from django.conf.urls.i18n import i18n_patterns

from catalog.sitemaps import get_sitemaps  # Импортируем функцию get_sitemaps
from django.contrib.auth import views as auth_views

sitemaps = get_sitemaps()  # Получаем динамически созданный словарь карт сайта

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('export-products-xlsx/', views.export_products_xlsx, name='export_products_xlsx'),
    path('admin/update_tracking_status/', update_tracking_status_view, name='update_tracking_status'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('feed_fb/', FacebookFeedView.as_view(), name='facebook_feed'),
    path('feed_google/', GoogleFeedView.as_view(), name='google_feed'),
    path('feed_rozetka/', RozetkaFeedView.as_view(), name='rozetka_feed'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('search/', product_search, name='product_search'),
    path('ajax/product-search/', AjaxProductSearch.as_view(), name='ajax_product_search'),  # AJAX поиск
    path('seller_cabinet/', views.seller_cabinet_main, name='seller_cabinet_main'),
    path('seller_cabinet/sale/', views.seller_cabinet_sales, name='seller_cabinet_sales'),
    path('seller_cabinet/sale/search_article/', views.search_article, name='search_article'),
    path('seller_cabinet/sale/add_item_to_sale/', views.add_item_to_sale, name='add_item_to_sale'),
    path('seller_cabinet/sale/remove_item_from_sale/', views.remove_item_from_sale, name='remove_item_from_sale'),
    path('seller_cabinet/sale/confirm_sale/', views.confirm_sale, name='confirm_sale'),
    path('seller_cabinet/sale/create_new_sale/', views.create_new_sale, name='create_new_sale'),  # Добавьте этот путь
    path('seller_cabinet/sale/get_pending_sale_items/', views.get_pending_sale_items, name='get_pending_sale_items'),
    path('seller_cabinet/sale/clear_sale/', views.clear_sale, name='clear_sale'),
    path('seller_cabinet/sale/get-daily-sales/', views.get_daily_sales, name='get_daily_sales'),
    path('seller_cabinet/sale/cancel_sale/', views.cancel_sale, name='cancel_sale'),
    path('seller_cabinet/preorder/', views.preorders, name='preorders'),
    path('api/preorder/<int:preorder_id>/toggle_shipped/', views.toggle_shipped, name='toggle_shipped'),
    path('api/preorder/<int:preorder_id>/toggle_receipt/', views.toggle_receipt, name='toggle_receipt'),
    path('api/get_preorders/', views.get_preorders, name='get_preorders'),
    path('api/preorder/create/', views.create_preorder, name='create_preorder'),
    path('api/preorder/<int:preorder_id>/update/', views.update_preorder, name='update_preorder'),
]

urlpatterns += i18n_patterns(
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/profile/', ProfileDetailView.as_view(), name='profile'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('', home, name='home'),  # URL для главной страницы
    path('add-to-cart/<str:custom_sku>/', views.add_to_cart, name='add_to_cart'),
    path('thank-you/', thank_you_page, name='thank_you_page'),
    path('cart/', cart_view, name='cart_view'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('remove-from-cart/<str:custom_sku>/', remove_from_cart, name='remove_from_cart'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sales/', sales, name='sales'),
    path('contacts/', contacts_page, name='contacts'),
    path('delivery_payment/', delivery_payment_page, name='delivery_payment_page'),
    path('privacy-policy/', privacy_policy_page, name='privacy_policy'),
    path('telegram/', telegram_page, name='telegram_page'),
    path('<slug:category_slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
