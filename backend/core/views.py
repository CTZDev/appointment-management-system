from rest_framework.response import Response
from .models import Pacient, Doctor, Specialty
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .serializers import DoctorDetailSerializer, PacientSerializer, DoctorSerializer, SpecialtySerializer
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_pacient(request):
    try:
        with transaction.atomic():
            serializer = PacientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def pacients(request):
    try:
        # select_related => Carga objetos (JOIN) en una sola consulta
        pacients = Pacient.objects.select_related("person", "person__user").filter(
            person__user__is_active=True)

        serializer = PacientSerializer(instance=pacients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
def change_pacient(request, pacient_id):
    try:
        with transaction.atomic():
            pacient = Pacient.objects.get(person_id=pacient_id)
            serializer = PacientSerializer(pacient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_pacient(request, pacient_id):
    try:
        pacient = Pacient.objects.select_related("person", "person__user").get(person_id=pacient_id)
        pacient.person.user.is_active = False
        pacient.person.user.save()

        serializer = PacientSerializer(pacient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pacient.DoesNotExist:
        return Response({"error": "Pacient no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def detail_pacient(request, pacient_id):
    try:
        pacient = Pacient.objects.get(person_id=pacient_id)
        serializer = PacientSerializer(pacient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_specialty(request):
    try:
        with transaction.atomic():
            serializer = SpecialtySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def specialties(request):
    try:
        specialties = Specialty.objects.filter(is_active=True)
        serializer = SpecialtySerializer(instance=specialties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def change_specialty(request, specialty_id):
    try:
        with transaction.atomic():
            Specialty = Specialty.objects.get(id=specialty_id)
            if Specialty.is_active is False:
                return Response({"error": "The specialty is not active."}, status=status.HTTP_404_NOT_FOUND)

            serializer = SpecialtySerializer(Specialty, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_specialty(request, specialty_id):
    try:
        specialty = Specialty.objects.get(id=specialty_id)
        if specialty.is_active is False:
            return Response({"error": "The specialty is not active."}, status=status.HTTP_404_NOT_FOUND)

        specialty.is_active = False
        specialty.save()
        serializer = SpecialtySerializer(specialty)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Specialty.DoesNotExist:
        return Response({"error": "Specialty not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def detail_specialty(request, specialty_id):
    try:
        specialty = Specialty.objects.get(id=specialty_id)
        if specialty.is_active is False:
            return Response({"error": "The specialty is not active."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpecialtySerializer(specialty)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_doctor(request):
    try:
        with transaction.atomic():
            serializer = DoctorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def doctors(request):
    try:
        # select_related => Carga objetos (JOIN) en una sola consulta
        doctors = Doctor.objects.select_related("person").all()
        print(doctors)

        serializer = DoctorDetailSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
def change_doctor(request, doctor_id):
    try:
        with transaction.atomic():
            doctor = Doctor.objects.get(person_id=doctor_id)
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#TODO: Arreglar el tema de relacion con user
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.select_related("person", "person__user").get(person_id=doctor_id)
        doctor.person.user.is_active = False
        doctor.person.user.save()

        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pacient.DoesNotExist:
        return Response({"error": "Doctor not Found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def detail_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.get(person_id=doctor_id)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
