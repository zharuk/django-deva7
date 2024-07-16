from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from catalog.models import PreOrder
from catalog.utils import notify_preorder_change


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
            'payment_received'
        ]

    def save(self, commit=True, request=None):
        obj = super().save(commit=False)
        if request and request.user.is_authenticated:
            obj.last_modified_by = request.user
        if commit:
            obj.save()
        return obj


class ProductSearchForm(forms.Form):
    query = forms.CharField(label=_('Поиск'), max_length=200, required=False)
