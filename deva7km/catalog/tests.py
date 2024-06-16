import requests


def track_package(tracking_number, bearer_token):
    url = f'https://www.ukrposhta.ua/status-tracking/0.0.1/statuses/{tracking_number}'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса

        data = response.json()
        return data  # Возвращаем ответ API (обычно это JSON с информацией о статусе трека)

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


# Пример использования:
if __name__ == '__main__':
    bearer_token = '0f5f4d65-89f6-3ceb-950f-3c3a0c686d50'  # Пример для PRODUCTION BEARER StatusTracking
    tracking_number = '0503905257970'

    result = track_package(tracking_number, bearer_token)
    if result:
        print(result)
