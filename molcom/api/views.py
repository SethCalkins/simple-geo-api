from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from decorators import *
from api import *
from api.models import *
from sources.arin import get_arin_info
from sources.ipdb import get_ip_info
import phonenumbers
import requests
from sources.ip_to_geo import get_geo

from django.forms.models import model_to_dict
from django.shortcuts import render


from util import levenshtein

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, link
from rest_framework import status
# from serializers import PostalCodeSerializer

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import filters
from rest_framework import generics
# from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle

class MyUserPermissions(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are

     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """

    def has_object_permission(self, request, view, obj):
        # check if user is owner
        return request.user == obj.user or request.user.is_superuser


class PostalCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostalCode
        fields = ('country', 'postal_code', 'region', 'latitude', 'longitude')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'definition')

class PostalCodeView(generics.ListAPIView):
#    country = self.kwargs['country']
    queryset = PostalCode.objects.all()
    throttle_classes = []
#    throttle_classes = (UserRateThrottle,)
#    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostalCodeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('postal_code', 'country', 'region')

class PostalCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PostalCode.objects.all()
    serializer_class = PostalCodeSerializer

class IpViewSet(viewsets.ViewSet):
    def list(self, request):
#        queryset = User.objects.all()
#        serializer = UserSerializer(queryset, many=True)
#        return Response(serializer.data)
        result = None
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def retrieve(self, request, pk=None):
#        result = (self.xform(m) for m in all_markets())
#    def get(self, request, *args, **kwargs):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        ip_addr = pk
        if ip_addr == '':
            ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

        result = get_geo(ip_addr)
        result = result.__dict__
        response = Response(result, status=status.HTTP_200_OK)
        return response

        # Any URL parameters get passed in **kwargs
#        myClass = CalcClass(get_arg1, get_arg2, *args, **kwargs)
#        result = myClass.do_work()
#        result = (self.xform(m) for m in all_markets())
#        response = Response(result, status=status.HTTP_200_OK)
#        return response

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (MyUserPermissions, )

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (MyUserPermissions, )
    def pre_save(self, obj):
        print 'START PRESAVE!!!'
        obj.user = self.request.user
        print 'PRESAVE END!!!'
#    serializer_class = UserSerializer

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X-Mashape-Authorization')
        if not username:
            return None
        user = username
        print 'auth', user

#        try:
#            user = User.objects.get(username=username)
#        except User.DoesNotExist:
#            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


def example_ip(request):
    c = {}
    return render(request, 'web/ip-example.html', c)

@csrf_exempt
@rest_json()
def blerg(request, s):
    pass

@csrf_exempt
@rest_json()
def dump(request):
    resp = {}
    resp['get'] = {k:unicode(v) for k,v in request.GET.items()}
    resp['meta'] = {k:unicode(v) for k,v in request.META.items()}
    print request.user
    return resp

@csrf_exempt
@rest_json()
def phonenumber(request, s):
    country = request.GET.get('country')
    p = phonenumbers.parse(s, country)
    possible = phonenumbers.is_possible_number(p)
    valid = phonenumbers.is_valid_number(p)
    resp = {
        'isPossible' : possible,
        'isValid' : valid,
    }
    remote = request.META.get('REMOTE_ADDR')
    user = request.META.get('HTTP_X_MASHAPE_USER')

    if possible and valid:
        resp_deets = {
            'countryCode' : p.country_code,
            'nationalNumber' : p.national_number,
            'e164' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164),
            'international' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'national' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.NATIONAL),
            'rfc3966' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.RFC3966),
            'location' : geocoder.description_for_number(p, "en"),
            'country' : geocoder.country_name_for_number(p, 'en')
        }
        resp = dict(resp.items() + resp_deets.items())
    return resp
#    qs = request.META.get('QUERY_STRING', '')
#    qs = API_KEY_STRIPPER.sub('', qs)
#    if qs:
#        qs = '?' + qs
#    uri = uri + qs
#    return sources.hds.get(uri)


import re
AS_PREFIX          = re.compile(r'^AS(\d+) ')

def get_org(ip_addr):
    try:
        resp = requests.get('http://ipinfo.io/%s/json' % ip_addr)
        if resp:
            org = resp.json().get('org')
            org = AS_PREFIX.sub('', org)
            return org
    except:
        return None

@csrf_exempt
@rest_json()
def ip_basic(request, s):
    ip_addr = s
    if ip_addr == '':
        ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    return get_geo(ip_addr).__dict__

@csrf_exempt
@rest_json()
def postalcode(request, country_code, postal_code):
    row = PostalCode.objects.get(country=country_code, postal_code=postal_code)
    d = row.__dict__
    del d['_state']
    del d['id']
    d['latitude'] = float(d['latitude'])
    d['longitude'] = float(d['longitude'])
    print d
    return d

    try:
        row = PostalCode.objects.get(country=country_code, postal_code=postal_code)
        return row.__dict__
    except Exception as e:
        return e
