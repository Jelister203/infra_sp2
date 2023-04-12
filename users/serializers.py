import re

from rest_framework import serializers

from users.models import User


class RegistrationSerializer(serializers.Serializer):
    """Сериализация регистрации пользователя и создания нового."""

    username = serializers.CharField(max_length=150, allow_blank=False)
    email = serializers.EmailField(max_length=254, allow_blank=False)

    def validate(self, data):
        username = data.get('username')
        if username == 'me':
            raise serializers.ValidationError("Can't use username 'me'")
        pattern = re.compile(r"^[\w.@+-]+")
        if not pattern.match(username):
            raise serializers.ValidationError("Bad symbols")
        return data


class TokenObtainSerializer(serializers.Serializer):
    """Сериализация получения токена пользователем."""

    username = serializers.CharField(max_length=150, allow_blank=False)
    confirmation_code = serializers.CharField(max_length=10, allow_blank=False)

    def validate(self, data):
        if data.get('username') == "":
            raise serializers.ValidationError("Empty username")
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор данных для юзеров."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор данных юзеров для администраторов."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
