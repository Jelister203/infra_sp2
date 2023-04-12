from datetime import datetime
from typing import OrderedDict

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Category`."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Genre`."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Title`."""

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'genre', 'year', 'description')
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'category', 'year'],
                message='Это произведение уже добавлено!',
            ),
        ]

    def to_representation(self, instance: Title) -> OrderedDict:
        """
        Форматирование вывода.

        Args:
            instance: Год создания произведения (указывает пользователь).

        Returns:
            Модифицированный вывод `category` и `genre`.

        """
        representation = super().to_representation(instance)
        representation['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug,
        }
        representation['genre'] = []
        for genre in instance.genre.all():
            representation['genre'].append(
                {'name': genre.name, 'slug': genre.slug},
            )
        return representation

    def validate_year(self, year: int) -> int:
        """
        Проверка даты.

        Args:
            year: Год создания произведения (указывает пользователь).

        Returns:
            Год создания произведения (проверено).

        Raises:
             ValidationError: Введите корректный год!
        """
        if year > datetime.now().year:
            raise serializers.ValidationError('Введите корректный год!')
        return year


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Review`."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Comment`."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации и создания нового пользователя."""

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Can't use username 'me'")
        return data

    class Meta:
        model = User
        fields = ['username', 'email']


class TokenObtainSerializer(serializers.Serializer):
    """Сериализация получения токена пользователем."""

    class Meta:
        fields = ['username', 'confirmation_code']
        read_only_fields = ['username', 'confirmation_code']


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализацор данных по юзерам."""

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
