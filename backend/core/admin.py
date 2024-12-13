from django.contrib import admin
from .models import Person, Pacient, Doctor

admin.site.register([Person, Pacient, Doctor])
