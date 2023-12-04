from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalog import views
from catalog.views import AllProductsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('all_products/', AllProductsView.as_view(), name='all_products'),
    path('categories/', views.category_list, name='category_list'),
    path('products/<str:category_slug>/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

