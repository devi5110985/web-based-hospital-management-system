from django.db import models

# Create your models here.

class Payment_Model(models.Model):
    name = models.CharField(max_length=100)
    
    amount = models.IntegerField()
    status  = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    


class Pyment_Details(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.name