from django.http import HttpResponse
from .models import Service, VehicleModel, Vehicle, Order, OrderLine
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import OrderCommentForm
from django.contrib.auth.decorators import login_required
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm, OrderForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
    return render(request, 'vehicles.html', context=context)

def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Vehicle, pk=automobilis_id)
    return render(request, 'vehicle.html', {'automobilis': automobilis})

def search(request):
    query = request.GET.get('query')
    search_results = Vehicle.objects.filter(Q(owner_name__icontains=query) | Q(vin__icontains=query) | Q(vehicle_model__model__icontains=query) | Q(vehicle_model__make__icontains=query) | Q(plate__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})

class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'uzsakymai'
    paginate_by = 4
    template_name = 'orders.html'



class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    context_object_name = 'uzsakymas'
    template_name = 'order.html'
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.object.id})

        # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.user = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


class MyOrderListView(generic.ListView):
    model = Order
    context_object_name = 'my_orders'
    template_name = 'my_orders.html'

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)



class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'uzsakymai'
    paginate_by = 10
    template_name = 'orders.html'



class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    context_object_name = 'uzsakymas'
    template_name = 'order.html'
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

        # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.user = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    # fields = ['vehicle', 'deadline', 'status']
    success_url = "/autoservisas/orders/"
    template_name = 'order_form.html'
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    # fields = ['vehicle', 'deadline', 'status']
    # success_url = "/autoservisas/orders/"
    template_name = 'order_form.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().client == self.request.user

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    context_object_name = 'uzsakymas'
    success_url = "/autoservisas/orders/"
    template_name = 'order_delete.html'

    def test_func(self):
        return self.get_object().client == self.request.user
