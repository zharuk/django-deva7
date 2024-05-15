from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from catalog import views
from catalog.feed_views import FacebookFeedView, GoogleFeedView, RozetkaFeedView
from catalog.views import home, contacts_page, \
    category_detail, product_detail, sales, telegram_page, \
    privacy_policy_page, cart_view, clear_cart, remove_from_cart, thank_you_page, delivery_payment_page

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('feed_fb/', FacebookFeedView.as_view(), name='facebook_feed'),
    path('feed_google/', GoogleFeedView.as_view(), name='google_feed'),
    path('feed_rozetka/', RozetkaFeedView.as_view(), name='rozetka_feed'),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

urlpatterns += i18n_patterns(
    path('', home, name='home'),
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
