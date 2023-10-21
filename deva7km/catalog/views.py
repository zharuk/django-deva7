from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Image


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# напишем функцию которая бы отрабатывала запрос на отображение картинок 'media/images/<str:path>'
def get_image_view(request, path):
    print(path)
    img = Image.objects.get(path='media/' + path)
    print(img)
    return render(request, 'catalog/image.html', {'img': img})
