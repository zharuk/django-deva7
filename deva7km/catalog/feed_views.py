from catalog.models import Product, ProductModification, Image, Category
from django.views import View
from django.http import HttpResponse
from django.template import loader
from django.utils.translation import activate
from django.conf import settings


class FacebookFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        # Получаем язык из параметра URL, по умолчанию украинский
        language = request.GET.get('lang', 'uk')

        # Проверяем, что язык поддерживается
        available_languages = [lang[0] for lang in settings.LANGUAGES]
        if language not in available_languages:
            language = 'uk'  # fallback на украинский

        # Активируем нужный язык
        activate(language)

        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()

        # Создаем копию request с нужным языком
        request_copy = request
        request_copy.LANGUAGE_CODE = language

        context = {
            'products': products,
            'modifications': modifications,
            'images': images,
            'request': request_copy,
            'language': language  # добавляем язык в контекст для шаблона
        }

        template = loader.get_template('fb_feed.xml')
        xml_content = template.render(context)
        response = HttpResponse(xml_content, content_type='application/xml')

        return response


class GoogleFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        context = {'products': products, 'modifications': modifications, 'images': images, 'request': request}
        template = loader.get_template('google_feed.xml')
        xml_content = template.render(context)
        response = HttpResponse(xml_content, content_type='application/xml')
        return response


class RozetkaFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        categories = Category.objects.all()
        context = {'products': products, 'modifications': modifications, 'images': images, 'categories': categories,
                   'request': request}
        template = loader.get_template('rozetka_feed.xml')
        xml_content = template.render(context)
        response = HttpResponse(xml_content, content_type='application/xml')
        return response


class OptFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        markup = request.GET.get('markup', '0')
        try:
            markup = int(markup)
        except ValueError:
            markup = 0

        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        categories = Category.objects.all()

        context = {
            'products': products,
            'modifications': modifications,
            'images': images,
            'categories': categories,
            'markup': markup,
            'request': request
        }
        template = loader.get_template('feed_opt.xml')
        xml_content = template.render(context)
        return HttpResponse(xml_content, content_type='application/xml')
