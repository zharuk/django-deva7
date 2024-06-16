import requests
from django.conf import settings
from django.utils import timezone
from catalog.models import PreOrder
import logging

logger_tracking = logging.getLogger('tracking')  # Логгер для отслеживания трекинга


def update_tracking_status():
    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)
    if not api_key:
        return

    url = 'https://api.novaposhta.ua/v2.0/json/'

    # Выбираем предзаказы, созданные в течение последних 10 дней
    ten_days_ago = timezone.now() - timezone.timedelta(days=10)
    preorders = PreOrder.objects.exclude(ttn='').filter(created_at__gte=ten_days_ago)

    for preorder in preorders:
        payload = {
            "apiKey": api_key,
            "modelName": "TrackingDocument",
            "calledMethod": "getStatusDocuments",
            "methodProperties": {
                "Documents": [
                    {
                        "DocumentNumber": preorder.ttn
                    }
                ]
            }
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if data['success']:
            status = data['data'][0]['Status']
            preorder.status = status
            preorder.save()

            # Логирование успешного обновления статуса трекинга
            logger_tracking.info(f"Обновлен статус для заказа {preorder.id}. Новый статус: {status}")
        else:
            # Логирование ошибок при запросе статуса трекинга
            logger_tracking.error(f"Ошибка при обновлении статуса для заказа {preorder.id}. Ответ API: {data}")

        # Логирование всех запросов и ответов API
        logger_tracking.debug(f"API запрос для заказа {preorder.id}: {payload}")
        logger_tracking.debug(f"API ответ для заказа {preorder.id}: {data}")
