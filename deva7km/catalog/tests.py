import requests


def get_tracking_status(ttn):
    api_key = '5cbd7778e124a4bb888fa25329535483'  # Замените на ваш API ключ
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
    data = response.json()

    if data['success']:
        status = data['data'][0]['Status']
        print(f"Статус посылки с ТТН {ttn}: {status}")
    else:
        print(f"Ошибка при получении статуса посылки с ТТН {ttn}: {data['errors'][0]['error']}")


if __name__ == "__main__":
    ttn = '59001345839441'  # Ваш номер ТТН для теста
    get_tracking_status(ttn)