from django.contrib.auth.models import User

class MashapeAuth:
    def process_request(self, request):
        mashape_username = request.META.get('HTTP_X_MASHAPE_USER')
        mashape_username = 'null'
        request.user = User.objects.get(username=mashape_username)

class DevAuth:
    def process_request(self, request):
        pass
#        request.user = User.objects.get(username='ojas')
#        request.META['x-user'] = 'ojas'
