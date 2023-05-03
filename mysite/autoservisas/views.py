from django.shortcuts import render
from django.http import HttpResponse
from .models import Service, VehicleModel, Vehicle, Order, OrderLine
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_vehicles = Vehicle.objects.count()
    num_orders = Order.objects.filter(status__exact='i').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_services': num_services,
        'num_vehicles': num_vehicles,
        'num_orders': num_orders,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)

def automobiliai(request):

    paginator = Paginator(Vehicle.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_automobiliai = paginator.get_page(page_number)
    automobiliai = paged_automobiliai
    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'automobiliai.html', context=context)

def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Vehicle, pk=automobilis_id)
    return render(request, 'automobilis.html', {'automobilis': automobilis})

def search(request):
    query = request.GET.get('query')
    search_results = Vehicle.objects.filter(Q(owner_name__icontains=query) | Q(vin__icontains=query) | Q(vehicle_model__model__icontains=query) | Q(vehicle_model__make__icontains=query) | Q(plate__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})

class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'uzsakymai'
    paginate_by = 4
    template_name = 'uzsakymai.html'



class OrderDetailView(generic.DetailView):
    model = Order
    context_object_name = 'uzsakymas'
    template_name = 'uzsakymas.html'