import logging
import requests
from django.conf import settings
from catalog.models import PreOrder

# Настройка логирования
logging.basicConfig(
    filename='/path/to/your/update_tracking.log',  # Укажите путь к файлу лога
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def update_tracking_status():
    api_key = getattr(settings, 'NOVA_POSHTA_API_KEY', None)  # Используем API ключ из настроек
    if not api_key:
        logging.error('API key not found in settings')
        return

    url = 'https://api.novaposhta.ua/v2.0/json/'

    preorders = PreOrder.objects.exclude(ttn='')

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
            logging.info(f'Status for TTN {preorder.ttn} updated to {status}')
        else:
            logging.error(f'Failed to update status for TTN {preorder.ttn}')

    logging.info('Successfully updated tracking statuses')
