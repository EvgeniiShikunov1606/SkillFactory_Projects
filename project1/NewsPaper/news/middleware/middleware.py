import pytz

from django.utils import timezone


class DetectMobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        # Простая проверка на наличие индикатора мобильного устройства в заголовках
        request.mobile = 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent

        response = self.get_response(request)
        return response


class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(response, 'template_name'):
            prefix = "mobile/" if request.mobile else "full/"
            response.template_name = prefix + response.template_name
        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
