from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone, formats


def format_ttn(ttn):
    ttn = ttn.replace(" ", "")  # Удаляем все пробелы
    formatted_ttn = " ".join([ttn[i:i + 4] for i in range(0, len(ttn), 4)])
    return formatted_ttn


def notify_preorder_change(sender, instance, event_type, **kwargs):
    channel_layer = get_channel_layer()

    created_at_local = timezone.localtime(instance.created_at)
    updated_at_local = timezone.localtime(instance.updated_at)
    created_at_formatted = formats.date_format(created_at_local, 'DATETIME_FORMAT')
    updated_at_formatted = formats.date_format(updated_at_local, 'DATETIME_FORMAT')
    last_modified_by = instance.last_modified_by.username if instance.last_modified_by else 'N/A'

    data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'text': instance.text,
        'drop': instance.drop,
        'created_at': created_at_formatted,
        'updated_at': updated_at_formatted,
        'receipt_issued': instance.receipt_issued,
        'shipped_to_customer': instance.shipped_to_customer,
        'payment_received': instance.payment_received,
        'status': instance.status,
        'ttn': instance.ttn,
        'last_modified_by': last_modified_by
    }

    async_to_sync(channel_layer.group_send)(
        'preorder_updates',
        {
            'type': 'notify_preorders_update',
            'event': event_type,
            'preorder': data,
        }
    )
    print(f"Sent {event_type} event for preorder {instance.id}")