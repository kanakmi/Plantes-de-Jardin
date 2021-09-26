from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class classify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_name = models.CharField(max_length=50)
    disease = models.CharField(max_length=50)
    accuracy = models.CharField(max_length=5)
    img = models.CharField(max_length=100)
    treatment = models.TextField()
