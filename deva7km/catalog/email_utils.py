from django.core.mail import send_mail
from django.template.loader import render_to_string

try:
    from deva7km.local_settings import ADMIN_EMAIL
except ImportError:
    from deva7km.prod_settings import ADMIN_EMAIL


def send_new_order_notification_email(order, cart_items, cart_total_price, cart_total_quantity):
    subject = f'Новый заказ на сайте ({order})'
    context = {
        'order': order,
        'cart_items': cart_items,
        'cart_total_price': cart_total_price,
        'cart_total_quantity': cart_total_quantity,
    }
    message = render_to_string('email/new_order_notification.html', context)
    recipient_list = [ADMIN_EMAIL]
    send_mail(subject, message, 'deva7km@gmail.com', recipient_list, html_message=message)
