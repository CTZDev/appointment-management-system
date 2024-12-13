from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.models import Pacient, Person

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        read_only_fields = ['id', 'date_joined', 'is_active']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        person = Person.objects.create(user=user)
        Pacient.objects.create(person=person)
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data.get('username')

        if 'email' in validated_data:
            new_email = validated_data.get('email')
            self.validate_email(new_email)
            instance.email = new_email
        instance.save()
        return instance

    def validate_email(self, value):
        request = self.context.get('request', None)
        is_register = self.context.get('is_register', False)  # Por defecto, no esta register

        if request:
            if not is_register and hasattr(request, 'user') and request.user.is_authenticated:
                # Validación para usuarios logueados
                if self.instance and self.instance.email == value:
                    return value
                if User.objects.filter(email=value).exclude(id=request.user.id).exists():
                    raise ValidationError("The email is already registered by another user.")
            elif is_register:
                # Validación para el registro
                if User.objects.filter(email=value).exists():
                    raise ValidationError("The email is already registered.")

        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise ValidationError("Las contraseñas no coinciden")
        return data

    def validate_current_password(self, value):
        user = self.context.get('user')  # El usuario viene desde views
        if not user.check_password(value):
            raise ValidationError("La contraseña actual no es correcta")
        return value

    def save(self):
        user = self.context.get('user')
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value
