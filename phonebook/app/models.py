from django.db import models

# Create your models here.

class Phonebook(models.Model):
    name = models.TextField()
    phn_num = models.IntegerField()