from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    
class Hall(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='hall_images/')
    
class Place(models.Model):
    hall = models.ForeignKey(Hall,on_delete=models.CASCADE)
    number = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
class Booking(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    