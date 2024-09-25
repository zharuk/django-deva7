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


CONTACT_METHOD_CHOICES = [
    ('viber', 'Viber'),
    ('telegram', 'Telegram'),
    ('messenger', 'Messenger'),
    ('direct', 'Direct'),
]

DELIVERY_METHOD_CHOICES = [
    ('nova_poshta', 'Новая Почта'),
    ('ukr_poshta', 'Укрпочта'),
]

PAYMENT_METHOD_CHOICES = [
    ('pre', 'Предоплата 150грн.'),
    ('full', 'Полная оплата'),
]


class OrderForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Фамилия', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_method = forms.MultipleChoiceField(
        label='Как с вами связаться?',
        choices=CONTACT_METHOD_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'})
    )
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    delivery_method = forms.ChoiceField(
        label='Способ доставки',
        choices=DELIVERY_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city = forms.CharField(label='Населенный пункт', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    post_office = forms.CharField(label='Отделение', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    comment = forms.CharField(
        label='Комментарий к заказу', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
