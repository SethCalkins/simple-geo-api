from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from decorators import *
from api import *
from api.models import PostalCode
import phonenumbers

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