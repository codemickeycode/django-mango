from django.conf import settings


class GlobalRequestMiddleware(object):
    """ A custom middleware that knows how to remember the request. """

    def process_request(self, request):
        settings.current_request = request

    def process_response(self, request, response):
        settings.current_request = None
        return response
