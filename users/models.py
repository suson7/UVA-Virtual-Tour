from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    discovery = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name='voted_locations', blank=True)
    description = models.CharField(max_length=250, default='Default Description')
    def __str__(self):
        return self.name


class Tour(models.Model):
    tour_name = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)
    premade = models.BooleanField(default=True)
    selected = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    user_name = models.CharField(max_length=200,null = True,default = "test")

# Create your models here.