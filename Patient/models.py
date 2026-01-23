from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.

class Patient_Regiser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Book_Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    doctor_name  = models.CharField(max_length=100)
    problem = models.CharField(max_length=100)
    upload_report = models.FileField(upload_to='media/' , validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    medication = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.name




