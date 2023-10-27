from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalog import views
from catalog.views import get_image_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path('media/<str:path>', get_image_view, name='image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

