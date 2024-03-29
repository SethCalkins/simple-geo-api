import views
from django.conf.urls import patterns, include, url

from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
#router.register(r'codes', )
router.register(r'codes', views.PostalCodeViewSet)
router.register('users', views.UserViewSet)
router.register('recipes', views.RecipeViewSet)
#router.register(r'users', views.UserViewSet)
#router.register(r'markets-orm', views.MarketViewSet, base_name='markets-orm')
router.register(r'ip2', views.IpViewSet, base_name='ip2')


# router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns( '',
    url(r'^', include(router.urls)),
# awesome generic stuff...
    url('^raw/postalcodes', views.PostalCodeView.as_view()),
#    url('^bs/(?P<country>.+)/(?P<postal_code>.+)$', views.PostalCodeView.as_view()),
    url( r'^phonenumber/(?P<s>.*)', views.phonenumber),
    url( r'^dump', views.dump),
    url( r'^postalcodes/(?P<country_code>.*)/(?P<postal_code>.*)', views.postalcode),
    url( r'^location/(?P<country_code>.*)/(?P<postal_code>.*)', views.postalcode),
    url( r'^ip/(?P<s>.*)', views.ip_basic),
)
