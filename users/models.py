
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
gender_choices = [
    ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=gender_choices, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics',
                              default='default.jpg', blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.user.username}) 