from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Car(models.Model):
    name = models.CharField(max_length=55)
    image = models.ImageField(upload_to='cars_images', null=True, blank=True, default="cars_images/no-image.jpg")
    year = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')

    def __str__(self):
        return f'{self.name} ({self.year}) - {self.owner}'