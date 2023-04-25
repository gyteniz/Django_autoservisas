from django.contrib import admin
from .models import (VehicleModel,
                     Vehicle,
                     Service,
                     Order,
                     OrderLine)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_model', 'plate', 'owner_name', 'vin')

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    # readonly_fields = ('id',)
    can_delete = False
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date']
    inlines = [OrderLineInline]
# ,'service', 'quantity'

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

# Register your models here.
admin.site.register(VehicleModel)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)