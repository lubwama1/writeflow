from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login as auth_login
from django.db import transaction

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensure the profile is saved if it already exists
        if hasattr(instance, 'profile'):
            instance.profile.save()
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

def on_user_logged_in(sender, request, user, **kwargs):
    if not request.user.is_authenticated:
        auth_login(request, user)
