import aiohttp
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.conf import settings
import logging
from datetime import timedelta

# Настройка логирования
logger_tracking = logging.getLogger('tracking')


async def get_tracking_status_from_api_nova_poshta(ttns, api_key):
    """Асинхронный запрос статуса посылки по API Nova Poshta."""
    url = 'https://api.novaposhta.ua/v2.0/json/'
    payload = {
        "apiKey": api_key,
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [{"DocumentNumber": ttn} for ttn in ttns]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    logger_tracking.info(f"Отправка запроса для TTNs {ttns}: {payload}")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response_text = await response.text()
            if response.status != 200:
                logger_tracking.error(
                    f"Неудачный запрос к API Nova Poshta для TTNs {ttns}. HTTP статус: {response.status}. Ответ: {response_text}")
                return None

            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                data = await response.json()
                logger_tracking.info(f"Получен ответ для TTNs {ttns}: {data}")
                return data
            else:
                logger_tracking.error(
                    f"Неверный тип ответа от API Nova Poshta для TTNs {ttns}. Получен тип: {content_type}. Ответ: {response_text}")
                return None


async def update_tracking_status(preorders):
    # Проверка и преобразование в список, если передан один объект
    if not isinstance(preorders, list):
        preorders = [preorders]

    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)
    carriers = {preorder.ttn: get_carrier(preorder.ttn) for preorder in preorders}
    ttns_nova_poshta = [ttn for ttn, carrier in carriers.items() if carrier == 'NovaPoshta']

    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    try:
        if not api_key and ttns_nova_poshta:
            logger_tracking.error("NOVA_POSHTА_API_KEY не установлен.")
            return

        # Фильтруем посылки для Nova Poshta
        preorders_to_update = []
        for preorder in preorders:
            if preorder.ttn in ttns_nova_poshta:
                if not preorder.status or preorder.status.strip() == "":
                    # Если статус пустой, обновляем независимо от времени последнего обновления
                    preorders_to_update.append(preorder)
                elif preorder.updated_at < one_hour_ago:
                    # Если статус не пустой и прошло больше часа с последнего обновления
                    preorders_to_update.append(preorder)

        # Получаем TTN для обновления
        ttns_to_update = [preorder.ttn for preorder in preorders_to_update]

        if ttns_to_update:
            data = await get_tracking_status_from_api_nova_poshta(ttns_to_update, api_key)
            if data and data.get('success'):
                for document in data.get('data', []):
                    ttn = document.get('Number')
                    status = document.get('Status')
                    if ttn and status:
                        preorder = next((p for p in preorders if p.ttn == ttn), None)
                        if preorder:
                            preorder_id = preorder.id  # Сохраняем идентификатор предзаказа
                            clean_status = status.strip().lower()  # Очистка и приведение к нижнему регистру
                            if "відправлення отримано" in clean_status:
                                await sync_to_async(preorder.delete)()  # Удаляем предзаказ
                                logger_tracking.info(
                                    f"Предзаказ {preorder_id} с TTN {ttn} был удален, так как статус 'Відправлення отримано'.")
                            else:
                                preorder.status = status  # Обновляем только статус без времени
                                await sync_to_async(preorder.save)()
                                logger_tracking.info(
                                    f"Обновлен статус для предзаказа {preorder_id}. Новый статус: {status}")

    except Exception as e:
        logger_tracking.error(f"Произошла ошибка при обновлении статуса: {e}")


def get_carrier(ttn):
    """Определение службы доставки по номеру ТТН."""
    if ttn.startswith('050'):
        return 'UkrPoshta'
    elif ttn.startswith('204'):
        return 'NovaPoshta'
    else:
        return 'Unknown'


async def get_tracking_status_from_api_ukrposhta(ttn):
    """Асинхронный запрос статуса посылки по API UkrPoshta.
       Здесь должен быть реальный запрос к API UkrPoshta, если он у вас есть."""
    # Пример заглушки для тестирования
    # Замените это на реальный код запроса к API UkrPoshta, если он доступен
    fake_response = {
        "success": True,
        "data": [
            {"Status": "НЕТ ДАННЫХ"}
        ]
    }
    return fake_response
