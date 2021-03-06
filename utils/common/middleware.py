class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('META', request.META)
        print('body', request.body.decode('utf-8'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print('response', response)
        print('content', response.content.decode('utf-8'))
        return response