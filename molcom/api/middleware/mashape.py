from django.contrib.auth.models import User
from django.conf import settings

class AuthenticationMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated():
            mashape_username = request.META.get('HTTP_X_MASHAPE_USER')
            mashape_proxy_secret = request.META.get('HTTP_X_MASHAPE_PROXY_SECRET')
            if mashape_username and mashape_proxy_secret == settings.MASHAPE_PROXY_SECRET:            
                username_fq = 'mashape_' + mashape_username
                try:
                    request.user = User.objects.get(username=username_fq)
                except User.DoesNotExist:
                    request.user = User.objects.create_user(username_fq, mashape_username + '@mashape')
        #           request.user = User(username=mashape_username)
