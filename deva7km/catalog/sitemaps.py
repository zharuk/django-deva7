# sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.translation import activate, get_language
from deva7km import settings
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(is_active=True).order_by('created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('product_detail', kwargs={'category_slug': obj.category.slug, 'product_slug': obj.slug})

    def get_urls(self, site=None, **kwargs):
        urls = []
        current_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            urls.extend(super().get_urls(site=site, **kwargs))
        activate(current_language)
        return urls


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            'home',
            'sales',
            'contacts',
            'delivery_payment_page',
            'privacy_policy',
            'telegram_page',
        ]

    def location(self, item):
        return reverse(item)

    def get_urls(self, site=None, **kwargs):
        urls = []
        current_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            urls.extend(super().get_urls(site=site, **kwargs))
        activate(current_language)
        return urls


def get_sitemaps():
    languages = [lang_code for lang_code, _ in settings.LANGUAGES]
    sitemaps = {}
    for language in languages:
        sitemaps.update({
            f'{language}_products': ProductSitemap,
            f'{language}_static_views': StaticViewSitemap,
        })
    return sitemaps
