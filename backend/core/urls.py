from django.urls import path
from . import views

urlpatterns = [
    path("pacients/", views.pacients, name="pacients"),
    path("add_pacient/", views.add_pacient, name="add_pacient"),
    path("change_pacient/<int:pacient_id>/", views.change_pacient, name="change_pacient"),
    path("delete_pacient/<int:pacient_id>/", views.delete_pacient, name="delete_pacient"),
    path("detail_pacient/<int:pacient_id>/", views.detail_pacient, name="detail_pacient"),

    path('specialties/', views.specialties, name='specialties'),
    path("add_specialty/", views.add_specialty, name="add_specialty"),
    path("change_specialty/<int:specialty_id>/",
         views.change_specialty, name="change_specialty"),
    path("delete_specialty/<int:specialty_id>/",
         views.delete_specialty, name="delete_specialty"),
    path("detail_specialty/<int:specialty_id>/",
         views.detail_specialty, name="detail_specialty"),

    path("doctors/", views.doctors, name="doctors"),
    path("add_doctor/", views.add_doctor, name="add_pacient"),
    path("change_doctor/<int:doctor_id>/", views.change_doctor, name="change_doctor"),
    path("delete_doctor/<int:doctor_id>/", views.delete_doctor, name="delete_pacient"),
    path("detail_doctor/<int:doctor_id>/", views.detail_doctor, name="detail_doctor"),
]
