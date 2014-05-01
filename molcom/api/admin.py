from django.contrib import admin
from models import *
from django_ace import AceWidget

def welcome(modeladmin, request, queryset):
    for obj in queryset:
        pass
#        send_welcome(obj)
welcome.short_description = "Re-send welcome message to customer"

class DirectCustomerAdmin(admin.ModelAdmin):
#   model = DirectCustomer
    action = []

class RecipeAdminForm(forms.ModelForm):
    definition = forms.CharField(widget=AceWidget(mode='json', theme='twilight', width='100%'))
    class Meta:
        model = Recipe
#            widgets = {
#          'by_admin':forms.RadioSelect
#        }

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    #list_display = ['title', 'status']
    #ordering = ['title']
    actions = [welcome]


admin.site.register(PostalCode)
admin.site.register(Recipe, RecipeAdmin)
