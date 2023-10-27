from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from catalog.models import Image, ProductModification


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# напишем функцию которая бы отрабатывала запрос на отображение картинок 'media/images/<str:path>'
def get_image_view(request, path):
    img = Image.objects.get(path='media/' + path)
    return render(request, 'catalog/image.html', {'img': img})

