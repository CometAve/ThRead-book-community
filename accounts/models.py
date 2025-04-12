from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(blank=True, null=True)
    weekly_reading_hours = models.PositiveIntegerField(blank=True, null=True)
    yearly_reading_count = models.PositiveIntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    interested_genres = models.CharField(max_length=600, blank=True)
