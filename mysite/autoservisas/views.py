from django.shortcuts import render
from django.http import HttpResponse
from .models import Service, VehicleModel, Vehicle, Order, OrderLine


# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_vehicles = Vehicle.objects.count()
    num_orders = Order.objects.filter(status__exact='i').count()

    context = {
        'num_services': num_services,
        'num_vehicles': num_vehicles,
        'num_orders': num_orders,
    }
    return render(request, 'index.html', context=context)

def automobiliai(request):
    automobiliai = Vehicle.objects.all()
    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'automobiliai.html', context=context)