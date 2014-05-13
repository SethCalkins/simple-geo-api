from django.core.management.base import BaseCommand, CommandError
from api.models import *
from api.sources.ipdb import *
from django.db import connections

class Command(BaseCommand):
    args = ''
    help = 'Manage the stats db'

    # registry|cc|type|start|value|date|status[|extensions...]

    def load(self, model, objs):
        model.objects.all().delete()
        model.objects.bulk_create(objs)

    def handle(self, *args, **options):
        cursor = connections['ipdb'].cursor()


#        sql = 'select * from city_blocks'

        if 1:
            print 'loading CityLocation...'
            cursor.execute('select * from city_location')
            objs = (CityLocation(id=item['loc_id'],
                    country=item['country_code'],
                    region_code=item['region_code'],
                    locality=item['city_name'],
                    postal_code=item['postal_code'],
                    latitude=item['latitude'],
                    longitude=item['longitude'],
                    metro_code=item['metro_code'],
                    area_code=item['area_code'],
                    ) for item in dictfetchall(cursor))
            self.load(CityLocation, objs)

        if 1:
            print 'loading IpBlock...'
            cursor.execute('select * from city_blocks')
            objs = (IpBlock(ip_start=item['ip_start'],
                    ip_end=item['ip_end'],
                    location_id=item['loc_id'],
                    source=INFO_SOURCE_MAXMIND,
                    ) for item in dictfetchall(cursor))
            self.load(IpBlock, objs)


