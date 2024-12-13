from .serializers import ChangePasswordSerializer, UserSerializer, PasswordResetRequestSerializer
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from decouple import config
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt


def create_user_data(request, is_register):
    serializer = UserSerializer(data=request.data, context={
                                "request": request, "is_register": is_register})
    if serializer.is_valid():
        user = serializer.save()
        # Generar token
        token, _ = Token.objects.get_or_create(user=user)
        return {"user": user, "token": token.key, "serializer": serializer}
    raise ValidationError(serializer.errors)


def update_user_data(user, data):
    serializer = UserSerializer(user, data=data, partial=True, context={"request": user})
    print(" --- ", serializer)
    if serializer.is_valid():
        serializer.save()
        return {"data": serializer.data}
    raise serializers.ValidationError(serializer.errors)


@api_view(["POST"])
# Config in settings (global)
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(User, email=request.data.get("email"))
    if not user.check_password(request.data.get("password")):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


# Users (Pacients for default)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def register(data):
    try:
        with transaction.atomic():
            new_user = create_user_data(data, is_register=False)
            return Response(
                {
                    "token": new_user["token"],
                    "user": new_user["serializer"].data,
                },
                status=status.HTTP_201_CREATED,
            )
    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"detail": f"Error inesperado: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def profile(request):
    serializer = UserSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def update_profile(request):
    try:
        with transaction.atomic():
            update_user = update_user_data(user=request.user, data=request.data)
            return Response({"user": update_user["data"]}, status=status.HTTP_200_OK)
    except serializers.ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@csrf_exempt
def logout_session(request):
    user_name = request.user.username if request.user.is_authenticated else "Usuario"
    token = Token.objects.get(user=request.user)
    token.delete()
    logout(request)

    return Response(
        {"message": f"Gracias por visitar nuestra página {user_name}. ¡Vuelva pronto 😊😊😊!"},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def users(request):
    users = User.objects.all().filter(is_active=True)
    serializer = UserSerializer(users, many=True)
    return Response({"users": serializer.data})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def detail_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found", code=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Config auth and permissions in settings (global) | Views for the admins
@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_user(data):
    with transaction.atomic():
        try:
            new_user = create_user_data(data, is_register=True)
            return Response({"user": new_user["serializer"].data}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Invalid data returned from create_user_data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def update_user(request, user_id):
    with transaction.atomic():
        try:
            user = User.objects.get(id=user_id)
            updated_user = update_user_data(user, request.data)
            return Response({"user": updated_user["data"]}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": "Invalid value provided"}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_active:
            return Response({"error": "User is already inactive"}, status=status.HTTP_409_CONFLICT)
        if user.is_superuser:
            return Response({"error": "Cannot deactivate a superuser"}, status=status.HTTP_403_FORBIDDEN)

        user.is_active = False
        user.save()

        serializer = UserSerializer(user, partial=True)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data, context={'user': user})

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password_request(request):
    serializer = PasswordResetRequestSerializer(data=request.data)

    if serializer.is_valid():
        user = get_object_or_404(User, email=serializer.data['email'])
        if not user.pk:
            return

        pk_bytes = user.pk.to_bytes(8, 'big')
        uid = urlsafe_base64_encode(force_bytes(pk_bytes))

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        reset_url = f"http://localhost:8000/api/v1/reset_password_confirm/{uid}/{token}/"
        print(f"Reset URL: {reset_url}")

        # Send the email
        send_mail(
            'Reset your password',
            f'Use this link to reset your password: {reset_url}',
            config('EMAIL_HOST_USER'),
            [user.email],
            fail_silently=False,
        )

        return Response({"detail": "Email sent on your address"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def reset_password_confirm(request, uidb64, token):
    try:
        uid_bytes = urlsafe_base64_decode(uidb64)
        uid = int.from_bytes(uid_bytes, 'big')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Link not valid"}, status=status.HTTP_400_BAD_REQUEST)

    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, token):
        return Response({"error": "Token not valid or expired"}, status=status.HTTP_400_BAD_REQUEST)

    new_password = request.data.get('new_password')
    repeat_password = request.data.get('repeat_password')
    if not new_password:
        return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not repeat_password:
        return Response({"error": "Repeat Password is required"}, status=status.HTTP_400_BAD_REQUEST)
    if new_password != repeat_password:
        return Response({"error": "The password do not match"}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
