#!/usr/bin/env python

import argparse
import logging
import fileinput
import sys
import requests
import json
import geoip2.database
from geoip2.errors import AddressNotFoundError

TEST_IPS = [t.strip() for t in """
158.151.208.58  
66.85.144.237   
220.181.158.174 
92.42.51.121    
49.230.83.151   
210.152.157.127 
195.219.251.157 
92.247.49.122   
183.60.244.29   
176.223.119.28  
113.17.173.11   
107.170.118.106 
183.60.244.37   
146.115.36.236  
209.112.7.18    
217.219.255.66  
196.3.132.92    
134.213.28.27   
195.78.211.2    
200.54.109.28   
82.221.105.6    
107.170.121.60
""".split('\n')]

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig()
#logger = logging.getLogger(__name__)
logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

DNB_DIRECT_ENDPOINT = 'http://dnbdirect-api.dnb.com/DnBAPI-14/rest/'

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.iteritems() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

def get_info_from_ip(ip_address):
    profound_url_format = 'http://api1.profound.net/ip/%s?key=038841C4E282AFC6'
    try:
        resp = requests.get(profound_url_format % ip_address).json()
    except:
        resp = {}
    return resp

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def direct(resource, data=None):
    url = DNB_DIRECT_ENDPOINT + resource
    headers = {
        'API-KEY' : 'f8ykv78dancm7kfvcv9xzkw4',
        'username' : 'api9700',
        'password' : 'welcome',
        'Accept-Encoding': 'UTF-8',
        'Content-Type': 'application/json',
        'Accept': '*/*',
    }
    if data:
        resp = requests.post(url, data=json.dumps(data), headers=headers)
    else:
        resp = requests.get(url, headers=headers)
    return resp.json()

#@cacheme(timeout=3600)
def ip_addr_to_geo(ip_addr):
    if ip_addr == '127.0.0.1' or not ip_addr:
        return None
    try:
        response = reader.city(ip_addr)
        return todict(response)
#        print response.__dict__
        return (response.country.iso_code, response.subdivisions.most_specific.iso_code)
    except AddressNotFoundError:
        logger.error('addr not found: %', ip_addr)
        return None

from pprint import pprint
import urllib2

def ip_mapping(ip_address):
    url = 'http://api.infochimps.com/web/analytics/ip_mapping/digital_element/domain?apikey=ojas-k_h2m15TgqI_VDujT3puJrYcC69&ip=' + ip_address
    print url
    return urllib2.urlopen(url).read()

if __name__ == "__main__":
    logger.debug('hi!')
    ip_address = '66.179.39.105' # Hoov
    ip_address = '67.198.16.146'

    for ip_addr in TEST_IPS:
#        pf = get_info_from_ip(ip_addr)
#        domain = pf.get('domain')
#        print ip_addr, domain, pf
        geo = ip_addr_to_geo(ip_addr)
        if geo:
            print
            print ip_addr
            print geo['location'].get('latitude'), geo['location'].get('longitude')
            print geo['location'].get('metro_code')
            print '%s %s' % (geo['country']['iso_code'], geo['city']['names'].get('en'))
            pf = get_info_from_ip(ip_addr)
            domain = pf.get('domain')
            print domain, pf
#            print 'Company' : 
#        pprint(geo['location'])

    exit()



#    r = direct('company/884114609')
    req = {
        'specialtyCriteria' : {
            'companyKeyword' : domain,
        }
    }

    r = direct('search/company/advanced/optional', req)
    pprint(r)
    exit()

    pprint(ip_addr_to_geo(ip_address))

#    print ip_mapping(ip_address)
    print get_info_from_ip(ip_address)

