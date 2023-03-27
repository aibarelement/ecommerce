import random

from django.http import HttpResponse


class HttpApiMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print('before first middleware')
        number = random.choice((1, 2))
        if number == 2:
            return HttpResponse({'message': 'ok'})

        response = self._get_response(request)
        print('after first middleware')

        return response


class SecondMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print('before second middleware')
        response = self._get_response(request)
        print('after second middleware')

        return response
