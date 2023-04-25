from django.contrib import admin
from .models import (VehicleModel,
                     Vehicle,
                     Service,
                     Order,
                     OrderLine)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_model', 'plate', 'owner_name')

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    # readonly_fields = ('id',)
    can_delete = False
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date']
    inlines = [OrderLineInline]
# ,'service', 'quantity'





# Register your models here.
admin.site.register(VehicleModel)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)