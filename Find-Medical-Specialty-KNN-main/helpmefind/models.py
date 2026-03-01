from django.db import models

# Create your models here.
class symptoms(models.Model):
    symptom = models.CharField(max_length=100)

class cities(models.Model):
    city = models.CharField(max_length=100)