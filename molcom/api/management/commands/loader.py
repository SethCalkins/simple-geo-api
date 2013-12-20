from django.core.management.base import BaseCommand, CommandError
from api.models import *
import csv
import json

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Manage the stats db'

    def handle(self, *args, **options):
        PostalCode.objects.all().delete()#clear()
        with open('../cityzip.csv', 'r') as f:
            reader = csv.DictReader(f)
            i = 0
            for r in reader:
                i += 1
                r = { k.lower() : v for k,v in r.items() }
                obj = {
                    'country' : 'US',
                    'postal_code' : r['postal'],
                    'city' : r['city'],
                    'region' : r['state'],
                    'latitude' : r['latitude'],
                    'longitude' : r['longitude']
                }
                if i % 1000 == 0:
                    print i
                p = PostalCode(**obj)
                try:
                    p.save()
                except Exception as e:
#                    print e
                    pass

