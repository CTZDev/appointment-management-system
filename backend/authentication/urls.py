from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("logout_session/", views.logout_session, name="logout_session"),
    path("users/", views.users, name="users"),
    path("detail_user/<int:id>/", views.detail_user, name="detail_user"),
    path("add_user/", views.add_user, name="add_user"),
    path("update_user/<int:user_id>/", views.update_user, name="update_user"),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path("change_password/", views.change_password, name="change_password"),
    path(
        "reset_password_request/",
        views.reset_password_request,
        name="reset_password_request",
    ),
    path('reset_password_confirm/<uidb64>/<token>/',
         views.reset_password_confirm, name='reset_password_confirm')
]
