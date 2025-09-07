from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Hall(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='hall_images/')
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Place(models.Model):
    hall = models.ForeignKey(Hall,on_delete=models.CASCADE)
    number = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.hall.name} - {self.number} ({self.category.name})'
    
class Booking(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    