from django.contrib import admin
from .models import (VehicleModel,
                     Vehicle,
                     Service,
                     Order,
                     OrderLine)

class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'model']
    list_filter = ['make']

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_model', 'plate', 'owner_name', 'vin']
    list_filter = ['owner_name', 'vehicle_model__make', 'vehicle_model__model']
    search_fields = ['plate', 'vin', 'vehicle_model__make', 'vehicle_model__model']

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    # readonly_fields = ('id',)
    can_delete = False
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date', 'client', 'deadline']
    search_fields = ['vehicle__plate', 'vehicle__vin', 'vehicle__vehicle_model__make']
    list_filter = ['vehicle__vehicle_model__make']
    list_editable = ['client', 'deadline']
    inlines = [OrderLineInline]

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

# Register your models here.
admin.site.register(VehicleModel, VehicleModelAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)