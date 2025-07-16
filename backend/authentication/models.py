from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.role}"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default="General Medicine")
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=20, unique=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    
    def __str__(self):
        return f"Patient {self.user.username} - {self.patient_id}"

class NurseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nurse_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default="General")
    shift = models.CharField(max_length=20, default="Day")
    
    def __str__(self):
        return f"Nurse {self.user.username} - {self.department}"