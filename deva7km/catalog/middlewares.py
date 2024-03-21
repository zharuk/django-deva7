# from django.conf import settings
# from django.utils.translation import activate
#
#
# class FrontendLanguageMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Проверяем, если запрос пришел из админки
#         print(1)
#         if request.path.startswith('/' + settings.ADMIN_URL):
#             print(2)
#             # Если запрос из админки, активируем язык по умолчанию (например, английский)
#             activate(settings.LANGUAGE_CODE)
#         else:
#             # Проверяем, новый ли пользователь по сессии
#             if 'language_selected' not in request.session:
#                 # Если пользователь новый и не выбрал язык по умолчанию, устанавливаем украинский язык
#                 activate('uk')
#                 request.session['language_selected'] = True
#                 print(request.session)
#             else:
#                 # В противном случае активируем язык, выбранный пользователем на фронтенде
#                 activate(request.LANGUAGE_CODE)
#                 print(request.session['language_selected'])
#
#         response = self.get_response(request)
#         return response
#
#
