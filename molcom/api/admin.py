from django.contrib import admin
from models import *

def welcome(modeladmin, request, queryset):
    for obj in queryset:
    	pass
#        send_welcome(obj)
welcome.short_description = "Re-send welcome message to customer"

class DirectCustomerAdmin(admin.ModelAdmin):
#	model = DirectCustomer
	action = []

class RecipeAdmin(admin.ModelAdmin):
    #list_display = ['title', 'status']
    #ordering = ['title']
    actions = [welcome]

admin.site.register(PostalCode)
admin.site.register(Recipe)
