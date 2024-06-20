import aiohttp
import asyncio

from asgiref.sync import sync_to_async
from django.utils import timezone
from django.conf import settings
import logging

# Настройка логирования
logger_tracking = logging.getLogger('tracking')


async def get_tracking_status_from_api_nova_poshta(ttn, api_key):
    """Асинхронный запрос статуса посылки по API Nova Poshta."""
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
            if response.status != 200:
                logger_tracking.error(
                    f"Неудачный запрос к API Nova Poshta для заказа с TTN {ttn}. HTTP статус: {response.status}")
                return None

            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                response_data = await response.json()
            else:
                response_text = await response.text()
                logger_tracking.error(
                    f"Неверный тип ответа от API Nova Poshta для заказа с TTN {ttn}. Получен тип: {content_type}. Ответ: {response_text}")
                return None

            return response_data


async def get_tracking_status_from_api_ukrposhta(ttn):
    """Асинхронный запрос статуса посылки по API UkrPoshta.
       Здесь должен быть реальный запрос к API UkrPoshta, если он у вас есть."""
    # Пример заглушки для тестирования
    # Замените это на реальный код запроса к API UkrPoshta, если он доступен
    fake_response = {
        "success": True,
        "data": [
            {"Status": "Посилка відправлена"}
        ]
    }
    return fake_response


# Пример функции обновления статуса, которая вызывает `get_tracking_status_from_api`

async def update_tracking_status(preorder):
    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)
    carrier = get_carrier(preorder.ttn)

    try:
        # Определяем, к какому API обращаться
        if carrier == 'NovaPoshta':
            if not api_key:
                logger_tracking.error("NOVA_POSHTA_API_KEY не установлен.")
                return

            # Получаем статус из API Nova Poshta
            data = await get_tracking_status_from_api_nova_poshta(preorder.ttn, api_key)

        elif carrier == 'UkrPoshta':
            # Получаем статус из API UkrPoshta
            data = await get_tracking_status_from_api_ukrposhta(preorder.ttn)

        else:
            logger_tracking.error(f"Неизвестный перевозчик для заказа {preorder.id} с TTN {preorder.ttn}.")
            return

        if not data:
            logger_tracking.error(f"Не удалось получить данные от API для заказа {preorder.id}.")
            return

        if not data.get('success'):
            logger_tracking.error(f"Ошибка при обновлении статуса для заказа {preorder.id}. Ответ API: {data}")
            return

        if not data.get('data'):
            logger_tracking.error(f"Ответ API не содержит данных для заказа {preorder.id}. Ответ API: {data}")
            return

        status = data['data'][0].get('Status')
        if not status:
            logger_tracking.error(f"Ответ API не содержит статус для заказа {preorder.id}. Ответ API: {data}")
            return

        # Исправленный формат времени
        current_time = timezone.localtime().strftime('%d.%m.%Y %H:%M:%S')
        current_admin_status = preorder.status

        # Обновляем статус, если он пустой или не содержит "Відправлення отримано"
        if not current_admin_status or "Відправлення отримано" not in status:
            status_with_time = f"{status} (обновлено: {current_time})"
            preorder.status = status_with_time
            await sync_to_async(preorder.save)()

            logger_tracking.info(f"Обновлен статус для заказа {preorder.id}. Новый статус: {status_with_time}")

        else:
            logger_tracking.info(
                f"Статус заказа {preorder.id} не был обновлен, так как текущий статус содержит '{status}'")

    except Exception as e:
        logger_tracking.error(f"Произошла ошибка при обновлении статуса для заказа {preorder.id}: {e}")


def get_carrier(ttn):
    """Определение службы доставки по номеру ТТН."""
    if ttn.startswith('0503'):
        return 'UkrPoshta'
    elif ttn.startswith('2045'):
        return 'NovaPoshta'
    else:
        return 'Unknown'
