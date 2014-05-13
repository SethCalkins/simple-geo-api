from django.core.management.base import BaseCommand, CommandError
from api.models import *
from api.sources.ip_to_geo import get_geo
import csv
import json

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
""".split('\n') if t]

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Manage the stats db'

    def handle(self, *args, **options):
        for ip_addr in TEST_IPS:
            resp = get_geo(ip_addr)
            print '%(ip)s %(country)s %(organization)s' % resp.__dict__

