from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(default="profile_pictures/default_pic.jpg", upload_to="profile_pictures/")

    def __str__(self):
        return self.user.username
