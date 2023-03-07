from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Deal(models.Model):
    deal_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.deal_name

class Location(models.Model):
    location_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.location_name

class Restaurant(models.Model):
    deals = models.ManyToManyField(Deal, related_name="deals")
    rest_name = models.CharField(max_length=30)
    rest_location = models.ForeignKey('Location', null=True, on_delete=models.CASCADE)
    image=models.ImageField(blank=True,null=True)
    def __str__(self) -> str:
        return self.rest_name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, primary_key=False)
    favorite_rest = models.ManyToManyField(Restaurant, related_name="restaurants")

    def __str__(self) -> str:
        return self.user.username
