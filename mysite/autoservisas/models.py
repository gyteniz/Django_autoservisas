from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=50)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"

class Vehicle(models.Model):
    plate = models.CharField(verbose_name="Valstybinis_Nr", max_length=6)
    vin = models.CharField(verbose_name="VIN_kodas", max_length=17)
    owner_name = models.CharField(verbose_name="Savininkas", max_length=50)
    owner = models.ForeignKey(to=User, verbose_name="Savininkas", on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_model = models.ForeignKey(to="VehicleModel",on_delete=models.SET_NULL, null=True)
    photo =models.ImageField(verbose_name="Nuotrauka", upload_to='vehicles', blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.plate})"

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'



class Order(models.Model):
    date = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atsaukta'),
        ('t', 'Tvirtinama'),
        ('i', 'Ivykdyta')
    )
    status = models.CharField(
        verbose_name="Busena",
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='t',
    )

    def total(self):
        total = 0
        lines = self.lines.all()
        for line in lines:
            total += line.suma()
        return total
    def __str__(self):
        return f"{self.vehicle} ({self.date})"

    class Meta:
        verbose_name = 'Uzsakymas'
        verbose_name_plural = 'Uzsakymai'

    def display_order(self):
        return ', '.join(order.vehicle for order in self.order.all())



class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name='lines')
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def __str__(self):
        return f"{self.order.vehicle} {self.order.date}: {self.service}"

    class Meta:
        verbose_name = 'Uzsakymo eilute'
        verbose_name_plural = 'Uzsakymo eilutes'

    def suma(self):
        return self.service.price * self.quantity


