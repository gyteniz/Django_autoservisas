from django.shortcuts import render
from django.http import HttpResponse
from .models import Service, VehicleModel, Vehicle, Order, OrderLine


# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_vehicle_models = VehicleModel.objects.all().count()
    num_vehicles = Vehicle.objects.all().count()
    num_orders = Order.objects.count()
    num_order_lines = OrderLine.objects.all().count()

    context = {
        'num_services': num_services,
        'num_vehicle_models': num_vehicle_models,
        'num_vehicles': num_vehicles,
        'num_orders': num_orders,
        'num_order_lines': num_order_lines,
    }
    return render(request, 'index.html', context=context)