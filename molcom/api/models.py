from django.db import models
from django import forms
from django.contrib.auth.models import User
import uuid

INFO_SOURCE_MAXMIND = 1
INFO_SOURCE_ARIN = 2
INFO_SOURCE_CHOICES = (
    (INFO_SOURCE_MAXMIND, 'MaxMind'),
    (INFO_SOURCE_ARIN, 'ARIN'),
)

class PostalCode(models.Model):
    country = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=10)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    class Meta:
        unique_together = (('country', 'postal_code', ),)
        __all__ = ['country', 'postal_code']
    def __unicode__(self):
        return unicode(self.country + ' ' + self.postal_code)

def make_uuid():
    return str(uuid.uuid4())

class Recipe(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)
    user = models.ForeignKey(User)
#    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50, )
    definition = models.CharField(max_length=4000)
    def __unicode__(self):
        return unicode(self.name)

class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    definition = forms.CharField(max_length=4000, widget=forms.Textarea)
    class Meta:
        model = Recipe

class CityLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=2)
    region_code = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    metro_code = models.CharField(max_length=10)
    area_code = models.CharField(max_length=10)
# 

def get_int_ip(ip_addr):
    try:
        ( o1, o2, o3, o4 ) = ip_addr.split('.')
        integer_ip = ( 16777216 * int(o1) ) + (    65536 * int(o2) ) + (      256 * int(o3) ) +              int(o4)
    except:
        integer_ip = None
    return integer_ip

import socket
import struct

def ip2int(addr):                                                               
    return struct.unpack("!I", socket.inet_aton(addr))[0]                       


def int2ip(addr):                                                               
    return socket.inet_ntoa(struct.pack("!I", addr)) 

class IpBlock(models.Model):
    ip_start = models.IntegerField()
    ip_end = models.IntegerField()
    source = models.IntegerField(choices=INFO_SOURCE_CHOICES)
    location = models.ForeignKey(CityLocation, null=True)

    @staticmethod
    def get_from_ip(ip_addr):
        int_ip = get_int_ip(ip_addr)
        if int_ip is not None:
            return IpBlock.objects.filter(ip_start__lte=int_ip, ip_end__gte=int_ip, source=INFO_SOURCE_MAXMIND).order_by('ip_start').first()
        return None

    @staticmethod
    def get_from_ip_alt(ip_addr):
        int_ip = get_int_ip(ip_addr)
        if int_ip is not None:
#            print int_ip, INFO_SOURCE_ARIN
#            mxs = IpBlock.objects.filter(ip_start__lte=int_ip, ip_end__gte=int_ip, source=INFO_SOURCE_ARIN)
#            print len(mxs)
            return IpBlock.objects.filter(ip_start__lte=int_ip, ip_end__gte=int_ip, source=INFO_SOURCE_ARIN).order_by('ip_start').first()
        return None

    class Meta:
        unique_together = (("ip_start", "source"),)

    def __unicode__(self):
        return unicode('%s - %s' % (int2ip(self.ip_start), int2ip(self.ip_end)))

class IpLog(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    ip_block = models.ForeignKey(IpBlock, null=True)

