import views
from django.conf.urls import patterns, include, url

from rest_framework import routers


router = routers.DefaultRouter()
#router.register(r'codes', )
router.register(r'codes', views.PostalCodeViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns( '',
    url(r'^', include(router.urls)),
# awesome generic stuff...
    url('^bs', views.PostalCodeView.as_view()),
#    url('^bs/(?P<country>.+)/(?P<postal_code>.+)$', views.PostalCodeView.as_view()),
    url( r'^phonenumber/(?P<s>.*)', views.phonenumber),
    url( r'^postalcodes/(?P<country_code>.*)/(?P<postal_code>.*)', views.postalcode),
)
