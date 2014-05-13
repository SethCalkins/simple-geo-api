from django.db import connections

def get_int_ip(ip_addr):
    try:
        ( o1, o2, o3, o4 ) = ip_addr.split('.')
        integer_ip = ( 16777216 * int(o1) ) + (    65536 * int(o2) ) + (      256 * int(o3) ) +              int(o4)
    except:
        integer_ip = None
    return integer_ip

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return (
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    )

def dictfetchone(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    row = cursor.fetchone()
    if row:
        return dict(zip([col[0] for col in desc], row))
    return {col[0]:None for col in desc}

def get_block_for_ip(ip_addr):
    MyModel.objects.filter(blah = blah)

def get_ip_info(ip_addr):
    cursor = connections['ipdb'].cursor()

    int_ip = get_int_ip(ip_addr)

    sql = """
SELECT     city_location.region_code,
           city_location.area_code,
           city_location.longitude,
           city_location.metro_code,
           city_location.latitude,
           city_location.postal_code,
           city_location.country_code,
           city_location.city_name as locality
FROM       city_blocks
INNER JOIN city_location on city_location.loc_id = city_blocks.loc_id
WHERE      %s BETWEEN ip_start and ip_end
"""

    cursor.execute(sql % (int_ip, ))

    resp = dictfetchone(cursor) #.fetchone()
    if resp is None:
        resp = {}
    return resp
