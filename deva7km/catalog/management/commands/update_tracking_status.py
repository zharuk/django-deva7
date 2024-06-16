# update_tracking_status.py

import requests
from catalog.models import PreOrder


def update_tracking_status():
    api_key = '5cbd7778e124a4bb888fa25329535483'  # Замените на ваш API ключ
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
