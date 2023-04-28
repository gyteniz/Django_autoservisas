from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobilis'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
]