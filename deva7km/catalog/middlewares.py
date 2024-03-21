from django.conf import settings
from django.utils.translation import activate


class FrontendLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, если запрос пришел из админки
        if request.path.startswith('/' + settings.ADMIN_URL):
            # Если запрос из админки, активируем язык по умолчанию (например, английский)
            activate(settings.LANGUAGE_CODE)
        else:
            # В противном случае активируем язык, выбранный пользователем на фронтенде
            if 'language_selected' not in request.session:
                # Если пользователь новый и не выбрал язык, устанавливаем украинский язык по умолчанию
                activate('uk')
                # Устанавливаем флаг выбора языка в сессии пользователя
                request.session['language_selected'] = True
            else:
                # Если язык уже был выбран пользователем, активируем его
                activate(request.LANGUAGE)

        response = self.get_response(request)
        return response


