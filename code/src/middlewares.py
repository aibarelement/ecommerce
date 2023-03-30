import httpx


class FirstMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # before
        request.client = httpx.Client()
        response = self._get_response(request, *args, **kwargs)
        # after
        return response
