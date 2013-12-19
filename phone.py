import phonenumbers
import json

from phonenumbers import carrier
from phonenumbers import geocoder
# https://github.com/daviddrysdale/python-phonenumbers

x = phonenumbers.parse("+442083661177", None)

y = phonenumbers.parse("020 8366 1177", "GB")

z = phonenumbers.parse("512-589-2634", 'US')

format = 'E164'
format = 'INTERNATIONAL'
format = ''
format = ''
#print phonenumbers[format]

phonenumbers.is_possible_number(z) 

phonenumbers.is_valid_number(z)

print dir(phonenumbers.PhoneNumberFormat)
print 
print x.country_code
print x
print str(x)
p = z
resp = {
	'countryCode' : p.country_code,
	'nationalNumber' : p.national_number,
	'isPossible' : phonenumbers.is_possible_number(p),
	'isValid' : phonenumbers.is_valid_number(p),
	'e164' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164),
	'international' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
	'national' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.NATIONAL),
	'rfc3966' : phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.RFC3966),
	'location' : geocoder.description_for_number(p, "en"),
	'country' : geocoder.country_name_for_number(p, 'en')
}

print json.dumps(resp, indent=2)
exit()
print y
print z

print repr(carrier.name_for_number(x, "en"))
print repr(carrier.name_for_number(y, "en"))
print repr(carrier.name_for_number(z, "en"))
