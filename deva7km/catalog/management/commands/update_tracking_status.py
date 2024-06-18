import requests
import time
import logging
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone

# Логирование
logger_tracking = logging.getLogger('tracking')


def update_tracking_status(preorder):
    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)
    if not api_key:
        return

    url = 'https://api.novaposhta.ua/v2.0/json/'

    # Попробуем получить статус из кэша
    cache_key = f"tracking_status_{preorder.ttn}"
    status_with_time = cache.get(cache_key)

    if status_with_time:
        # Если статус есть в кэше, обновляем и сохраняем предзаказ
        preorder.status = status_with_time
        preorder.save()
        logger_tracking.info(f"Обновлен статус из кэша для заказа {preorder.id}. Новый статус: {status_with_time}")
        return

    # Если статуса нет в кэше, делаем запрос к API
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

    # Добавим задержку перед запросом
    time.sleep(1)

    response = requests.post(url, json=payload)
    data = response.json()

    if data['success']:
        status = data['data'][0]['Status']
        current_time = timezone.localtime().strftime('%d-%m-%Y %H:%M:%S')

        # Не обновляем статусы, содержащие "Відмова від отримання" и "Відправлення отримано"
        if "Відмова від отримання" in status or "Відправлення отримано" in status:
            logger_tracking.info(f"Статус заказа {preorder.id} не был обновлен, так как он содержит '{status}'")
            return

        # Добавляем время обновления к статусу
        status_with_time = f"{status} (обновлено: {current_time})"
        preorder.status = status_with_time
        preorder.save()

        # Кэшируем статус на 10 минут
        cache.set(cache_key, status_with_time, timeout=600)

        # Логирование успешного обновления статуса трекинга
        logger_tracking.info(f"Обновлен статус для заказа {preorder.id}. Новый статус: {status_with_time}")
    else:
        # Логирование ошибок при запросе статуса трекинга
        logger_tracking.error(f"Ошибка при обновлении статуса для заказа {preorder.id}. Ответ API: {data}")

    # Логирование всех запросов и ответов API
    logger_tracking.debug(f"API запрос для заказа {preorder.id}: {payload}")
    logger_tracking.debug(f"API ответ для заказа {preorder.id}: {data}")
