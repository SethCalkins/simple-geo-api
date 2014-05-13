from api.models import IpBlock, IpLog, ip2int, INFO_SOURCE_ARIN, PostalCode
from api.sources.arin import get_arin_info
from api.util import levenshtein

ARIN_COUNTRIES = (
'AI',
'AQ',
'AG',
'BS',
'BB',
'BM',
'BV',
'CA',
'KY',
'DM',
'GD',
'GP',
'HM',
'JM',
'MQ',
'MS',
'PR',
'KN',
'LC',
'VC',
'SH',
'PM',
'TC',
'US',
'UM',
'VG',
'VI',
)

class IpGeoResponse(object):
    ip = None
    locality = None
    region_code = None
    postal_code = None
    country = None
    latitude = None
    longitude = None
    organization = None
    pass
#    def __init__(self):
#        self.data = []

def get_geo(ip_addr):
    resp = IpGeoResponse()
    resp.ip = ip_addr
    resp.organization = None

    is_arin_country = False

    ip_block = IpBlock.get_from_ip(ip_addr)
    if ip_block:
        location = ip_block.location
        if location:
            resp.locality = location.locality
            resp.region_code = location.region_code
            resp.postal_code = location.postal_code
            resp.country = location.country
            # area_code
            # metro_code
            resp.latitude = location.latitude
            resp.longitude = location.longitude

            is_arin_country = resp.country in ARIN_COUNTRIES

#            resp['locality'] = ip_block.locality
#        resp['block'] = unicode(ip_block)
#        resp['block_location'] = model_to_dict(ip_block.location)

    if is_arin_country:
        info = get_arin_info('ip', ip_addr)
        if info is not None:
            arin_block = IpBlock(ip_start=ip2int(info['net']['startAddress']['$']), ip_end=ip2int(info['net']['endAddress']['$']), source=INFO_SOURCE_ARIN)
    #        print arin_block
            existing_arin_block = IpBlock.get_from_ip_alt(ip_addr)
            if existing_arin_block is None:
                arin_block.save()

            obj = None

            if 'orgRef' in info['net']:            
                org_name = info['net']['orgRef']['@name']
                org_id = info['net']['orgRef']['@handle']
#                print info['net']['orgRef']['$']
#                exit()
                org_info = get_arin_info('org', org_id)
                detail_resp = org_info['org']
                obj = {
                    'locality' : detail_resp['city']['$'],
                    'postal_code' : detail_resp['postalCode']['$'],
                    'country' : detail_resp['iso3166-1']['code2']['$'],
                    'region_code' : detail_resp.get('iso3166-2', {}).get('$'),
                    'organization' : detail_resp['name']['$'],
        #                    'city' : detail_resp['streetAddress']['line'],
                }
            elif 'customerRef' in info['net']:
                org_name = info['net']['customerRef']['@name']
                org_id = info['net']['customerRef']['@handle']
                org_info = get_arin_info('customer', org_id)
                detail_resp = org_info['customer']
                obj = {
                    'locality' : detail_resp['city']['$'],
                    'postal_code' : detail_resp['postalCode']['$'],
                    'country' : detail_resp['iso3166-1']['code2']['$'],
                    'region_code' : detail_resp.get('iso3166-2', {}).get('$'),
                    'organization' : detail_resp['name']['$'],
        #                    'city' : detail_resp['streetAddress']['line'],
                }

            # if we got details from ARIN, merge into resp
            if obj:
                if detail_resp:
                    print
                    print detail_resp
                    print
                for k, v in obj.items():
                    setattr(resp, k, v)

                # use our postal code database...
                pcs = PostalCode.objects.filter(country = resp.country, postal_code=resp.postal_code)
                best_match = None
                best_match_dist = 3
                for pc in pcs:
                    dist = levenshtein(pc.city.lower(), resp.locality.lower())
                    if dist < best_match_dist:
                        best_match_dist = dist
                        best_match = pc

                if best_match:
                    resp.latitude = best_match.latitude
                    resp.longitude = best_match.longitude
                    resp.locality = best_match.city
                    resp.postal_code = best_match.postal_code
                else:
                    resp.latitude = None
                    resp.longitude = None
        
    if ip_block:
        rec = IpLog.objects.get_or_create(ip=ip_addr)
        print rec
#        resp['rec']



    return resp
