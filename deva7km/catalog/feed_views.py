from django.http import HttpResponse
from django.template import loader
from django.views import View
from catalog.models import Product, ProductModification, Image, Category


class FacebookFeedView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        modifications = ProductModification.objects.all()
        images = Image.objects.all()
        context = {'products': products, 'modifications': modifications, 'images': images, 'request': request}
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
