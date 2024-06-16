import requests
from django.conf import settings
from django.utils import timezone
from catalog.models import PreOrder

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
