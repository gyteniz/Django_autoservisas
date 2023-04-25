from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name}"


class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=50)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Vehicle Model"
        verbose_name_plural = "Verhicle Models"

class Vehicle(models.Model):
    plate = models.CharField(verbose_name="Valstybinis_Nr", max_length=6)
    vin = models.CharField(verbose_name="VIN_kodas", max_length=17)
    owner_name = models.CharField(verbose_name="Savininkas", max_length=50)
    vehicle_model = models.ForeignKey(to="VehicleModel",on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.plate})"



class Order(models.Model):
    date = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle} ({self.date})"


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE)
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def __str__(self):
        return f"{self.order.vehicle} {self.order.date}: {self.service}"