from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalog import views
from catalog.views import AllProductsView, home, about_page, contacts_page, delivery_page, payment_page, \
    category_detail, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('all_products/', AllProductsView.as_view(), name='all_products'),
    path('about/', about_page, name='about'),
    path('contacts/', contacts_page, name='contacts'),
    path('delivery/', delivery_page, name='delivery'),
    path('payment/', payment_page, name='payment'),
    path('<slug:category_slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

