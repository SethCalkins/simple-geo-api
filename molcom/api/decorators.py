import logging

from xml.sax.saxutils import escape
from json import JSONEncoder, loads

from functools import wraps
from django.core.cache import cache
import json
import decimal
from django.http import HttpResponse, HttpRequest, Http404
#from sources.direct_auth import auth_api_key

# logging.basicConfig(level=logging.INFO)

import logging
logger = logging.getLogger(__name__)

class DjangoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
#        if isinstance(o, Model):
#            s = serialize('json', [o])
#            o = loads(s)[0]
#            id = o['pk']
#            o = o['fields']
##            o['id'] = id
#            return o
        return super(DjangoJSONEncoder, self).default(o)

def _json(f):
    response = HttpResponse(content_type='application/json')
#    response.content = json.dumps(f) if not isinstance(f, (str, unicode)) else f
    response.content = json.dumps(f, cls=DjangoJSONEncoder)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'API-KEY, username, password'
    return response

def _xml(f):
    response = HttpResponse(content_type='text/xml')
    response.content = f
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'API-KEY, username, password'
    return response


class AccessDeniedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def cacheme(cachekeyprefix = None, timeout=None):
    def decorator(f):
        @wraps(f)
        def cacher(*args, **kwargs):
            std_args = args[1:] if len(args) and isinstance(args[0], HttpRequest) else args
            params = [cachekeyprefix or f.func_name] + list(std_args) + ['%s:%s' % (k, kwargs.get(k)) for k in sorted(kwargs.keys())]
            # The non-keyword parameters used to call the function are used as the keys
            cachekey = cache.make_key(':'.join(map(str,params)))
            if cachekey in cache:
                print 'hit for %s' % cachekey
                logger.debug('Cache hit for key [%s]' % cachekey)
                return cache.get(cachekey)
            else:
                print 'miss for %s' % cachekey
                logger.debug('Cache miss for key [%s, %s]' % (cachekey, timeout))
                val = f(*args, **kwargs)
                if timeout is None:
                    cache.set(cachekey, val)
                else:
                    cache.set(cachekey, val, timeout=timeout)
                return val
        return cacher
    return decorator

def xxx__cacheme(cachekeyprefix=None, timeout=None):
    if timeout is None and type(cachekeyprefix) is int:
        timeout = cachekeyprefix
        cachekeyprefix = None
    print cachekeyprefix, timeout

    def decorator(f):
#        if cachekeyprefix is None:
#            cachekeyprefix = f.func_name
        @wraps(f)
        def cacher(*args, **kwargs):
            if cachekeyprefix is None:
                cachekeyprefix = f.func_name
            # The non-keyword parameters used to call the function are used as the keys
            cachekey = cache.make_key(':'.join(map(str,(cachekeyprefix,) + args[1:])))
            if cachekey in cache:
                logging.info('Cache hit for key [%s]' % cachekey)
                return cache.get(cachekey)
            else:
                logging.info('Cache miss for key [%s, %s]' % (cachekey, timeout))
                val = f(*args, **kwargs)
                cache.set(cachekey, val, timeout=timeout)
                return val
        return cacher
    return decorator


def xxxcacheme(cachekeyprefix, timeout=None):
    def decorator(f):
        @wraps(f)
        def cacher(*args, **kwargs):
#            key = json.dumps({'prefix' : cachekeyprefix, 'args' : args[1:], 'kwargs': ['%s:%s' % (k, kwargs.get(k)) for k in sorted(kwargs.keys())] })
            std_args = args[1:] if len(args) and isinstance(args[0], HttpRequest) else args
            params = [cachekeyprefix] + list(std_args) + ['%s:%s' % (k, kwargs.get(k)) for k in sorted(kwargs.keys())]
            print params
#            print key
#            params += 
#            print 'args', len(args), kwargs
            # The non-keyword parameters used to call the function are used as the keys
            cachekey = cache.make_key(':'.join(map(str,params)))
            if cachekey in cache:
                logging.info('Cache hit for key [%s]' % cachekey)
                return cache.get(cachekey)
            else:
                logging.info('Cache miss for key [%s, %s]' % (cachekey, timeout))
                val = f(*args, **kwargs)
                cache.set(cachekey, val, timeout=timeout)
                return val
        return cacher
    return decorator

def rest_json():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.method == 'OPTIONS':
                return _json({})
            try:
                val = f(*args, **kwargs)
                return _json(val)
            except Http404:
                raise
            except Exception as e:
                raise
                logger.exception('rest_json error')
                response = _json({'error': { 'message' : '%s' % e } })
                response.status = 403
                return response


        return wrapper
    return decorator

def rest_xml():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.method == 'OPTIONS':
                return _xml('<xml/>')
            try:
                val = f(*args, **kwargs)
                return _xml(val)
            except Http404:
                raise
            except Exception as e:
                response = _xml('<error><message>%s</message></error>' % escape(unicode(e)))
                response.status = 403
                return response


        return wrapper
    return decorator

def auth():
    def decorator(f):
        @wraps(f)
        def auther(*args, **kwargs):
            request = args[0]
            dnb_api_key = request.META.get('HTTP_API_KEY', request.GET.get('api-key'))
#            ok = auth_api_key(dnb_api_key)
            ok = True
            if ok:
                val = f(*args, **kwargs)
                return val
            else:
                raise Exception('access denied')
#                return {'error': { 'message' : 'access denied'} }
        return auther
    return decorator