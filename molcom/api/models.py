from django.db import models
from django import forms
from django.contrib.auth.models import User
import uuid

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