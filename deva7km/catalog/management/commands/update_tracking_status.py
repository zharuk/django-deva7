import aiohttp
import asyncio

from aiohttp import payload
from django.utils import timezone
from django.conf import settings
import logging

# Настройка логирования
logger_tracking = logging.getLogger('tracking')


async def get_tracking_status_from_api(ttn, api_key):
    """Асинхронный запрос статуса посылки по API."""
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

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            response_data = await response.json()
            return response_data


async def update_tracking_status(preorder):
    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)
    if not api_key:
        logger_tracking.error("NOVA_POSHTА_API_KEY не установлен.")
        return

    # Добавим задержку перед запросом, если это необходимо
    await asyncio.sleep(1)

    # Получаем статус из API
    data = await get_tracking_status_from_api(preorder.ttn, api_key)

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

    # Проверяем текущий статус в админке
    current_admin_status = preorder.status

    # Если текущий статус пустой или новый статус не "Відправлення отримано", обновляем статус
    if not current_admin_status or "Відправлення отримано" not in status:
        # Добавляем время обновления к статусу
        status_with_time = f"{status} (обновлено: {current_time})"
        preorder.status = status_with_time
        await preorder.asave()  # Предполагаем, что метод asave() асинхронный

        # Логирование успешного обновления статуса трекинга
        logger_tracking.info(f"Обновлен статус для заказа {preorder.id}. Новый статус: {status_with_time}")

    else:
        logger_tracking.info(f"Статус заказа {preorder.id} не был обновлен, так как текущий статус содержит '{status}'")

    # Логирование всех запросов и ответов API
    logger_tracking.debug(f"API запрос для заказа {preorder.id}: {payload}")
    logger_tracking.debug(f"API ответ для заказа {preorder.id}: {data}")
