from django.shortcuts import render
from .serializers import ScheduleSerializer, AppointmentSerializer
from .models import Schedule, Appointment
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser


def add_schedule(request):
    return None

def schedules(request):
    return None

def change_schedule(request):
    return None

def delete_schedule(request):
    return None

def detail_schedule(request):
    return None

def add_appointment(request):
    return None

def view_appointment(request):
    return None

def change_appointment(request):
    return None

def delete_appointment(request):
    return None

def detail_appointment(request):
    return None
