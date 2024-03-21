from django.conf import settings
from django.utils.translation import activate


class FrontendLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, если запрос пришел из админки
        if request.path.startswith('/' + settings.ADMIN_URL):
            # Если запрос из админки, активируем язык по умолчанию (например, английский)
            activate('ru')
        else:
            # В противном случае активируем язык, выбранный пользователем на фронтенде
            activate(request.LANGUAGE_CODE)

        response = self.get_response(request)
        return response

