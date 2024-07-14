from django import forms
from django.utils.translation import gettext_lazy as _

from catalog.models import PreOrder


class PreOrderForm(forms.ModelForm):
    class Meta:
        model = PreOrder
        fields = [
            'full_name',
            'text',
            'drop',
            'receipt_issued',
            'ttn',
            'shipped_to_customer',
            'status',
            'payment_received'  # Добавляем новое поле
        ]


class ProductSearchForm(forms.Form):
    query = forms.CharField(label=_('Поиск'), max_length=200, required=False)
