import asyncio

import requests
import logging
from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import PreOrder
from django.db.models import Q

NOVA_POSHTA_API_URL = "https://api.novaposhta.ua/v2.0/json/"
NOVA_POSHTA_API_KEY = settings.NOVA_POSHTA_API_KEY  # Убедитесь, что здесь используется правильное имя

logger = logging.getLogger('tracking')


def get_tracking_status(ttns):
    payload = {
        "apiKey": NOVA_POSHTA_API_KEY,
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [{"DocumentNumber": ttn} for ttn in ttns]
        }
    }
    response = requests.post(NOVA_POSHTA_API_URL, json=payload)
    return response.json()


async def update_tracking_status():
    logger.info("Starting to update tracking statuses.")
    now = timezone.now()

    # Удаляем предзаказы старше 30 дней или с статусом "Відправлення отримано"
    await sync_to_async(PreOrder.objects.filter(
        Q(status__icontains="Відправлення отримано") | Q(created_at__lt=now - timezone.timedelta(days=30))
    ).delete)()
    logger.info("Old preorders or received ones deleted.")

    # Получаем все TTN из базы данных, которые были обновлены не менее 30 минут назад
    thirty_minutes_ago = now - timezone.timedelta(minutes=30)
    all_ttns = await sync_to_async(list)(
        PreOrder.objects.filter(updated_at__lt=thirty_minutes_ago).values_list('ttn', flat=True)
    )
    logger.info(f"Retrieved TTNs from database: {all_ttns}")

    ttn_mapping = {ttn.replace(" ", ""): ttn for ttn in all_ttns if ttn and ttn.replace(" ", "").isdigit()}
    cleaned_ttns = list(ttn_mapping.keys())
    logger.info(f"Cleaned TTNs: {cleaned_ttns}")

    if not cleaned_ttns:
        logger.info("No valid TTNs found for updating status.")
        return

    # Разбиваем список TTN на порции по 100 элементов
    chunk_size = 25
    chunks = [cleaned_ttns[i:i + chunk_size] for i in range(0, len(cleaned_ttns), chunk_size)]

    for chunk in chunks:
        status_response = get_tracking_status(chunk)
        logger.info(f"Status response from Nova Poshta: {status_response}")

        if not status_response.get('success'):
            logger.error("Failed to get status from Nova Poshta.")
            continue

        status_data_list = status_response.get('data', [])
        logger.info(f"Status data list: {status_data_list}")

        for status_data in status_data_list:
            cleaned_ttn_number = status_data['Number']
            status = status_data['Status']

            original_ttn_number = ttn_mapping.get(cleaned_ttn_number)
            if not original_ttn_number:
                logger.warning(f"No original TTN found for cleaned TTN {cleaned_ttn_number}")
                continue

            try:
                preorders = await sync_to_async(list)(
                    PreOrder.objects.filter(ttn=original_ttn_number, updated_at__lt=thirty_minutes_ago)
                )
                if not preorders:
                    logger.warning(f"PreOrder with TTN {original_ttn_number} does not exist or was recently updated.")
                    continue
            except Exception as e:
                logger.error(f"Error retrieving PreOrder with TTN {original_ttn_number}: {e}")
                continue

            for preorder in preorders:
                preorder.status = status
                preorder.tracking_status = status
                preorder.updated_at = now

                await sync_to_async(preorder.save)()
                logger.info(f"PreOrder with TTN {original_ttn_number} updated successfully.")

        # Добавляем задержку 1 секунду между обработкой чанков
        await asyncio.sleep(1)