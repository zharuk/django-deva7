from aiohttp import payload
from django.core.cache import cache
from django.utils import timezone
import requests
import logging
import time
from django.conf import settings

# Настройка логирования
logger_tracking = logging.getLogger('tracking')


def get_tracking_status_from_api(ttn, api_key):
    """Запрос статуса посылки по API."""
    url = 'https://api.novaposhta.ua/v2.0/json/'
    payload = {
        "apiKey": api_key,
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [
                {
                    "DocumentNumber": ttn
                }
            ]
        }
    }
    response = requests.post(url, json=payload)
    return response.json()


def update_tracking_status(preorder):
    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)
    if not api_key:
        logger_tracking.error("NOVA_POSHTA_API_KEY не установлен.")
        return

    # Попробуем получить статус из кэша
    cache_key = f"tracking_status_{preorder.ttn}"
    status_with_time = cache.get(cache_key)

    if status_with_time:
        # Если статус есть в кэше, обновляем и сохраняем предзаказ
        preorder.status = status_with_time
        preorder.save()
        logger_tracking.info(f"Обновлен статус из кэша для заказа {preorder.id}. Новый статус: {status_with_time}")
        return

    # Добавим задержку перед запросом, если это необходимо
    time.sleep(1)

    # Получаем статус из API
    data = get_tracking_status_from_api(preorder.ttn, api_key)

    if not data.get('success'):
        # Логирование ошибок при запросе статуса трекинга
        logger_tracking.error(f"Ошибка при обновлении статуса для заказа {preorder.id}. Ответ API: {data}")
        return

    if not data.get('data'):
        # Логирование отсутствия данных в ответе API
        logger_tracking.error(f"Ответ API не содержит данных для заказа {preorder.id}. Ответ API: {data}")
        return

    status = data['data'][0].get('Status')
    if not status:
        # Логирование отсутствия статуса в ответе API
        logger_tracking.error(f"Ответ API не содержит статус для заказа {preorder.id}. Ответ API: {data}")
        return

    current_time = timezone.localtime().strftime('%d.%m.%Y %H:%M:%S')

    # Игнорируем статусы "Відправлення отримано" и "Відмова від отримання"
    if "Відправлення отримано" in status:
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

    # Логирование всех запросов и ответов API
    logger_tracking.debug(f"API запрос для заказа {preorder.id}: {payload}")
    logger_tracking.debug(f"API ответ для заказа {preorder.id}: {data}")
