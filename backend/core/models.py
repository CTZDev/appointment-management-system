from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='person',
        null=True,
        blank=True
    )
    dni = models.CharField(
        unique=True,
        validators=[RegexValidator(r'^\d{8}$', 'The DNI must contain exactly 8 characters.')],
        db_index=True,
        max_length=8,
        null=True,
    )
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    phone_validator = RegexValidator(r'^\d{9}$', 'The phone number must have 9 digits')
    phone = models.CharField(max_length=9, validators=[phone_validator], blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',
    )
    direction = models.CharField(max_length=250, blank=True, null=True)
    register_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"Person (DNI: {self.dni})"


class Pacient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A positivo'),
        ('A-', 'A negativo'),
        ('B+', 'B positivo'),
        ('B-', 'B negativo'),
        ('AB+', 'AB positivo'),
        ('AB-', 'AB negativo'),
        ('O+', 'O positivo'),
        ('O-', 'O negativo'),
    ]

    person = models.OneToOneField(Person, on_delete=models.CASCADE,
                                  related_name='pacient', primary_key=True)
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        default='O+',
    )
    contact_phone_validator = RegexValidator(
        r'^\d{9}$', 'The number of emergency contact phone must have 9 digits')
    contact_phone = models.CharField(max_length=9, validators=[
                                     contact_phone_validator], blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    clinical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        user_data = self.person.first_name.join(
            self.person.last_name) if self.person.first_name != None else self.person.user.username
        return f"Pacient - {user_data}"


class Specialty(models.Model):
    description = models.CharField(max_length=250, blank=True, null=True, unique=True)
    register_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description if self.description else "No description"


class Doctor(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE,
                                  related_name='doctor', primary_key=True)
    specialties = models.ManyToManyField(Specialty, related_name='doctors')

    cmp = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(
            r'^[A-Za-z0-9]+$', 'The CMP must contain only alphanumeric characters.')]
    )

    rne = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(
            r'^[A-Za-z0-9]+$', 'The RNE must contain only alphanumeric characters.')]
    )

    def __str__(self):
        return f"Doctor {self.person.first_name} {self.person.last_name}"
