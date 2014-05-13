import requests
from ..decorators import cacheme
import logging
logger = logging.getLogger(__name__)

@cacheme()
def get_arin_info(entity, ip_addr):
    url_format = 'http://whois.arin.net/rest/%s/%s.json'
    try:
        resp = requests.get(url_format % (entity, ip_addr))
        if resp:
            resp = resp.json()
            return resp
    except:
    	logger.exception('error getting json from arin')
        return None

