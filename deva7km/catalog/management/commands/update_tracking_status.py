import requests
from django.conf import settings
from catalog.models import PreOrder


def update_tracking_status():
    api_key = settings.NOVA_POSHTA_API_KEY  # Используем API ключ из настроек
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
            print(f'Status for TTN {preorder.ttn} updated to {status}')
        else:
            print(f'Failed to update status for TTN {preorder.ttn}')
