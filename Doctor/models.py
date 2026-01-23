from django.db import models

# Create your models here.

class AddDoctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    experience = models.IntegerField()
    qualification = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.specialization})'
    


class Doctor_Medication(models.Model):
    p_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    prescription = models.CharField(max_length=1000)
    admitted = models.CharField(max_length=100)
    medication = models.CharField(max_length=20)

    def __str__(self):
        return self.name