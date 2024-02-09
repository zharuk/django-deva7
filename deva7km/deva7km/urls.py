from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalog.views import home, about_page, contacts_page, delivery_page, payment_page, \
    category_detail, product_detail, sales, telegram_page, FacebookFeedView, GoogleFeedView, \
    RozetkaFeedView, privacy_policy_page

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('feed_fb/', FacebookFeedView.as_view(), name='facebook_feed'),
    path('feed_google/', GoogleFeedView.as_view(), name='google_feed'),
    path('feed_rozetka/', RozetkaFeedView.as_view(), name='google_feed'),
]

urlpatterns += (i18n_patterns(path('', home, name='home'),
                              path('ckeditor/', include('ckeditor_uploader.urls')),
                              path('sales/', sales, name='sales'),
                              path('about/', about_page, name='about'),
                              path('contacts/', contacts_page, name='contacts'),
                              path('delivery/', delivery_page, name='delivery'),
                              path('payment/', payment_page, name='payment'),
                              path('privacy-policy/', privacy_policy_page, name='privacy_policy'),
                              path('telegram/', telegram_page, name='telegram_page'),
                              path('<slug:category_slug>/', category_detail, name='category_detail'),
                              path('<slug:category_slug>/<slug:product_slug>/', product_detail,
                                   name='product_detail'), ))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
