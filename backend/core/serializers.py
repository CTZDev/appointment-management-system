from authentication.serializers import UserSerializer
from .models import Person, Doctor, Pacient, Specialty
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
import uuid


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Person
        fields = ['id', 'dni', 'first_name', 'last_name',
                  'birth_date', 'phone', 'gender', 'direction', 'user']
        read_only_fields = ['id']

    def validate_dni(self, value):
        if len(value) != 8:
            raise ValidationError("The DNI must contain exactly 8 characters.")
        if self.instance and self.instance.dni == value:
            return value
        if Person.objects.filter(dni=value).exists():
            raise ValidationError("The DNI is already registered.")
        return value

    def validate_birth_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValidationError("The date format is invalid. It must be YYYY-MM-DD.")

        current_year = date.today().year
        minimum_year = 1940
        if value.year < minimum_year or value.year > current_year:
            raise ValidationError(f"The year must be between {minimum_year} and {current_year}.")
        return value

    def validate_gender(self, value):
        valid_choices_gender = [choice[0] for choice in self.Meta.model.GENDER_CHOICES]
        if value not in valid_choices_gender:
            raise ValidationError(
                "The entered gender is invalid. Valid options: M, F, O."
            )
        return value

    def validate_direction(self, value):
        if len(value) > 250:
            raise ValidationError("The address must have a maximum of 250 characters.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)

        if not user_data:
            user = User.objects.create(
                username=f"user_{uuid.uuid4().hex[:16]}",
                email=f"test_{uuid.uuid4().hex[:16]}@test.com",
            )
            user.set_password("1234")
            user.save()
        else:
            password = user_data.pop('password', None)
            user = User.objects.create(**user_data)
            if password:
                user.set_password(password)

        person = Person.objects.create(user=user, **validated_data)
        return person

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        # Actualiza los datos de 'Person'
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Si hay datos de usuario, actualiza tambien el usuario
        if user_data:
            instance.user.update(user_data)
        return instance


class PacientSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Pacient
        fields = ["person", "blood_group", "contact_phone", "allergies", "clinical_history"]

    def validate_blood_group(self, value):
        valid_choices_blood = [choice[0] for choice in self.Meta.model.BLOOD_GROUP_CHOICES]
        if value not in valid_choices_blood:
            raise ValidationError(
                f"The entered blood group is invalid. Valid options: {
                    ', '.join(valid_choices_blood)}."
            )
        return value

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        person = PersonSerializer.create(PersonSerializer(), validated_data=person_data)
        pacient = Pacient.objects.create(person=person, **validated_data)
        return pacient

    def update(self, instance, validated_data):
        person_data = validated_data.pop('person', None)

        if person_data:
            instance.person = PersonSerializer().update(instance.person, person_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'description']
        read_only_fields = ['id']

    def validate_description(self, value):
        if len(value) > 250:
            raise ValidationError(
                'The description of the specialty should have a maximum of 250 characters.')
        return value


class DoctorSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    specialties = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Specialty.objects.filter(is_active=True)
    )

    class Meta:
        model = Doctor
        fields = ["person", "cmp", "rne", "specialties"]

    def validate_field(self, value, field_name):
        if value is not None:
            if len(value) > 12:
                raise ValidationError(f"The {field_name} must have a maximum of 12 characters.")
            if not value.isalnum():
                raise ValidationError(
                    f"The {field_name} must only contain alphanumeric characters.")
        return value

    def validate_cmp(self, value):
        return self.validate_field(value, "CMP")

    def validate_rne(self, value):
        return self.validate_field(value, "RNE")

    def create(self, validated_data):
        person_data = validated_data.pop("person")
        specialties_data = validated_data.pop("specialties", [])

        person = Person.objects.create(**person_data)
        doctor = Doctor.objects.create(person=person, **validated_data)

        if specialties_data:
            doctor.specialties.set(specialties_data)
        return doctor

    def update(self, instance, validated_data):
        person_data = validated_data.pop("person", None)
        specialties_data = validated_data.pop("specialties", None)

        if person_data:
            for attr, value in person_data.items():
                setattr(instance.person, attr, value)
            instance.person.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if specialties_data is not None:
            instance.specialties.set(specialties_data)
        return instance


class DoctorDetailSerializer(DoctorSerializer):
    specialties_details = SpecialtySerializer(many=True, read_only=True, source='specialties')

    class Meta(DoctorSerializer.Meta):
        fields = DoctorSerializer.Meta.fields + ["specialties_details"]

    # Sobrescribir el campo specialties para no incluirlo en el serializer
    specialties = serializers.CharField(write_only=True, required=False)
