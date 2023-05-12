from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vehicles/', views.automobiliai, name='vehicles'),
    path('vehicles/<int:automobilis_id>', views.automobilis, name='vehicle'),
    path('search/', views.search, name='search'),
    path('my_orders/', views.MyOrderListView.as_view(), name='my_orders'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('orders/new', views.OrderCreateView.as_view(), name='order_new'),
    path('orders/<int:pk>/update', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/newline', views.OrderLineCreateView.as_view(), name='newline'),
]