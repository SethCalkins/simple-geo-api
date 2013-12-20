import views
from django.conf.urls import patterns, include, url

urlpatterns = patterns( '',
    url( r'^phonenumber/(?P<s>.*)', views.phonenumber),
    url( r'^postalcodes/(?P<country_code>.*)/(?P<postal_code>.*)', views.postalcode),
)
