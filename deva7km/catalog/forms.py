from django import forms
from django.utils.translation import gettext_lazy as _


class OrderForm(forms.Form):
    name = forms.CharField(label=_('Имя'), max_length=100)
    surname = forms.CharField(label=_('Фамилия'), max_length=100)
    phone = forms.CharField(label=_('Телефон'), max_length=15)
    email = forms.EmailField(label=_('Email'), required=False)

    CONTACT_CHOICES = {
        'telegram': _('Telegram'),
        'whatsapp': _('WhatsApp'),
        'viber': _('Viber'),
        'sms': _('SMS'),
    }
    contact_method = forms.MultipleChoiceField(label=_('Связь с клиентом'), choices=CONTACT_CHOICES.items(),
                                               widget=forms.CheckboxSelectMultiple)

    DELIVERY_CHOICES = {
        'nova_poshta': _('новая почта'),
        'ukrposhta': _('укрпочта'),
    }
    delivery_method = forms.ChoiceField(label=_('Способ доставки'), choices=DELIVERY_CHOICES.items(),
                                        widget=forms.RadioSelect)

    city = forms.CharField(label=_('Населенный пункт'), max_length=100)
    post_office = forms.CharField(label=_('Отделение почты'), max_length=100)

    PAYMENT_CHOICES = {
        'prepayment_150': _('предоплата 150 грн'),
        'full_prepayment': _('полная предоплата'),
    }
    payment_method = forms.ChoiceField(label=_('Способ оплаты'), choices=PAYMENT_CHOICES.items(),
                                       widget=forms.RadioSelect)

    comment = forms.CharField(label=_('Комментарий к заказу'), required=False)




class ProductSearchForm(forms.Form):
    query = forms.CharField(label=_('Поиск'), max_length=200, required=False)
