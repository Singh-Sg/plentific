from ast import mod
from django.db import models

# Create your models here.

class PlentificRecord(models.Model):
    uuid = models.CharField(max_length=200)
    amount = models.IntegerField()
    create_date = models.DateTimeField()
    location = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    col6 = models.CharField(max_length=100, null=True, blank=True)
    col7 = models.CharField(max_length=100, null=True, blank=True)
    col8 = models.CharField(max_length=100, null=True, blank=True)
    col9 = models.CharField(max_length=100, null=True, blank=True)
    col10 = models.CharField(max_length=100, null=True, blank=True)
    col11 = models.CharField(max_length=100, null=True, blank=True)
    col12 = models.CharField(max_length=100, null=True, blank=True)
    col13 = models.CharField(max_length=100, null=True, blank=True)
    col14 = models.CharField(max_length=100, null=True, blank=True)
    col15 = models.CharField(max_length=100, null=True, blank=True)
    col16 = models.CharField(max_length=100, null=True, blank=True)


class Ab(models.Model):
    name = models.CharField(max_length=200)
