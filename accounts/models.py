from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='userprofile')
    profile_img=models.ImageField(upload_to='profile',blank=True)
    bio = models.CharField(max_length=160,blank=True)
    about = models.TextField(blank=True)