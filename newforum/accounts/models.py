from django.db import models
from django.contrib.auth.models import User



class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    picture=models.ImageField(blank=True)
    birthdate=models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    def __repr__(self):
        return self.user

       