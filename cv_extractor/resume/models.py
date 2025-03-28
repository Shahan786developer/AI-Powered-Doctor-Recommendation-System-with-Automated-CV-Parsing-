# models.py

from django.db import models
from django.contrib.auth.models import User

class CV(models.Model):
    cv_file = models.FileField(upload_to='cv_files/')  # File field for the uploaded CV file

    def __str__(self):
        return f"{ self.cv_file.name}"  # Return a more descriptive string for the CV

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location")
    address = models.CharField(max_length=255)  # Full address
    latitude = models.FloatField()  # Latitude for geolocation
    longitude = models.FloatField()  # Longitude for geolocation

    def __str__(self):
        return f"{self.user.username}'s Location"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cv_file = models.FileField(upload_to='cvs/', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    work_experience = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField('Skill', blank=True)
    pmc_number = models.CharField(max_length=20, null=True, blank=True)
  
    ai_recommendation = models.TextField(null=True, blank=True)
    isverified = models.BooleanField(null=True,default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
