from .models import Schedule, Appointment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import date, datetime
from core.serializers import DoctorSerializer, PacientSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Schedule
        fields = ['id', 'date_start', 'date_end', 'time_start', 'time_end', 'doctor']
        read_only_fields = ['id', 'register_at', 'updated_at']

    def validate(self, data):
        if data['date_start'] > data['date_end']:
            raise ValidationError('The date end should be greater than the date start.')
        if data['time_start'] > data['time_end']:
            raise ValidationError('The time end should be greater than the time start.')
        if not data['doctor']:
            raise ValidationError('The doctor is required.')
        return data

    def validate_date_start(self, value):
        if not isinstance(value, date):
            raise ValidationError('The date start should be in the format YYYY-MM-DD.')
        return value

    def validate_date_end(self, value):
        if not isinstance(value, date):
            raise ValidationError('The date end should be in the format YYYY-MM-DD.')
        return value

    def validate_time_start(self, value):
        if not isinstance(value, datetime):
            raise ValidationError('The time start should be in the format HH:MM:SS.')
        return value

    def validate_time_end(self, value):
        if not isinstance(value, datetime):
            raise ValidationError('The time end should be in the format HH:MM:SS.')
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    pacient = PacientSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ['id', 'register_at', 'updated_at']

    def validate(self, data):
        if data['scheduled_date'] > data['cancelled_date']:
            raise ValidationError(
                "The cancelled date should be greater than the scheduled date.")
        if not data['doctor']:
            raise ValidationError("The doctor is required.")
        if not data['pacient']:
            raise ValidationError("The pacient is required.")
        return data

    def validate_scheduled_date(self, value):
        if not isinstance(value, date):
            raise ValidationError("The scheduled date should be in the format YYYY-MM-DD.")
        return value

    def validate_cancelled_date(self, value):
        if not isinstance(value, date):
            raise ValidationError("The cancelled date should be in the format YYYY-MM-DD.")
        return value

    def validate_state(self, value):
        if value not in Appointment.APPOINTMENT_STATE_CHOICES:
            raise ValidationError(
                "The state should be one of the following: pending, cancelled, completed.")
        return value
