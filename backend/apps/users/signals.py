from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)   # Function will be executed after saving new User instance
def create_profile(sender, instance, created, **kwargs):
    """
    Profile is created while new User instance appears.
    sender - User model
    instance - new instance of User model
    created - True or False

    Signal must be registered in apps.py
    """
    if created:
        Profile.objects.create(user=instance)