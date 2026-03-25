from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    profile_user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='abcd')

    


class WeatherData(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    city = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    weather = models.CharField(max_length=10,default=0)
    speed = models.CharField(max_length=10,default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"weather in {self.city} at {self.timestamp}"