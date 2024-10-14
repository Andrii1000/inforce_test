from django.http import JsonResponse


class AppVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        app_version = request.headers.get('Build-Version')
        if app_version:
            if app_version == '1.0':
                request.version = 'old'
            else:
                request.version = 'new'
        else:
            return JsonResponse({"error": "Build-Version header is required"}, status=400)

        response = self.get_response(request)
        return response
