from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(
        upload_to="profile_pictures", default="profile_pictures/profile.jpg")

    def __str__(self):
        return str(self.user)
