from django.db import models

# Create your models here.
class offline_counter(models.Model):
    date = models.DateField(primary_key=True)
    query1 = models.IntegerField()
    query2 = models.IntegerField()
    query3 = models.IntegerField()
    model = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class offline_confirmed(models.Model):
    date = models.DateField(primary_key=True)
    query1 = models.IntegerField()
    query2 = models.IntegerField()
    query3 = models.IntegerField()
    model = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
