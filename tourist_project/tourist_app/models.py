from django.db import models


from django.db import models
import json

class TouristDes(models.Model):
    placename = models.CharField(max_length=100)
    weather = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    maplink = models.URLField()
    description = models.TextField()
    img = models.ImageField(upload_to='images/')

class TouristImage(models.Model):
    tourist_des = models.ForeignKey(TouristDes, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')