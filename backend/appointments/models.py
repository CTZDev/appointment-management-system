from django.db import models
from core.models import Doctor, Pacient


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='doctor_schedule')
    description = models.CharField(max_length=250, blank=True, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    register_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        first_name = self.doctor.person.first_name or "Unknown"
        last_name = self.doctor.person.last_name or "Unknown"
        return f"Doctor {first_name} {last_name} - Schedule: {self.date_start} to {self.date_end}, {self.time_start} to {self.time_end}"


class Appointment(models.Model):
    APPOINTMENT_STATE_CHOICES = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='doctor_appointment')
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE,
                                related_name='pacient_appointment')
    scheduled_date = models.DateField()
    cancelled_date = models.DateField(blank=True, null=True)
    register_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10, choices=APPOINTMENT_STATE_CHOICES, default='pending')

    def __str__(self):
        doctor_name = f"{self.doctor.person.first_name} {self.doctor.person.last_name}"
        pacient_name = f"{self.pacient.person.first_name} {self.pacient.person.last_name}"
        return f"Appointment: Doctor {doctor_name} - Pacient {pacient_name} on {self.scheduled_date}"
