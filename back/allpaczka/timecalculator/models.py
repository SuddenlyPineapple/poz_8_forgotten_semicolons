from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    auction_url = models.CharField(max_length=200, null=True)
    img_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address

class Package(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='packages')
    places = models.ManyToManyField(Place, through='Route', related_name='packages')
    start_date = models.DateField(null=True)

    def __str__(self):
        return self.name
    
class Route(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date_joined = models.DateField()

