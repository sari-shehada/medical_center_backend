class CharsetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_response(response)
        return response

    def process_response(self, response):
        if 'application/json' in response.get('Content-Type', ''):
            response['Content-Type'] = 'application/json; charset=utf-8'
