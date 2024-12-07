from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Phonebook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn_num= models.IntegerField()
    
class Otp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.TextField()