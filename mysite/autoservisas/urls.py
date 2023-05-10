from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.OrderListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.OrderDetailView.as_view(), name='uzsakymas'),
    path('search/', views.search, name='search'),
    path('my_orders/', views.MyOrderListView.as_view(), name='my_orders'),
    path('register/', views.register, name='register'),
]