from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    auction_url = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Package(models.Model):
    items = models.ManyToManyField(Product)
    


