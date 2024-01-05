from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalog.views import home, about_page, contacts_page, delivery_page, payment_page, \
    category_detail, product_detail, sales, all_products, telegram_page, FacebookFeedView, GoogleFeedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed_fb/', FacebookFeedView.as_view(), name='facebook_feed'),
    path('feed_google/', GoogleFeedView.as_view(), name='google_feed'),
    path('', home, name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('all_products/', all_products, name='all_products'),
    path('sales/', sales, name='sales'),
    path('about/', about_page, name='about'),
    path('contacts/', contacts_page, name='contacts'),
    path('delivery/', delivery_page, name='delivery'),
    path('payment/', payment_page, name='payment'),
    path('telegram/', telegram_page, name='telegram_page'),
    path('<slug:category_slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),  # Обновлено
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
