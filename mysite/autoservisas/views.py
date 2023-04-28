from django.shortcuts import render
from django.http import HttpResponse
from .models import Service, VehicleModel, Vehicle, Order, OrderLine
from django.shortcuts import render, get_object_or_404
from django.views import generic


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

def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Vehicle, pk=automobilis_id)
    context = {
        'automobilis': automobilis
    }
    return render(request, 'automobilis.html', context=context)

class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'uzsakymai'
    template_name = 'uzsakymai.html'

class OrderDetailView(generic.DetailView):
    model = Order
    context_object_name = 'uzsakymas'
    template_name = 'uzsakymas.html'