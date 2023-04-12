from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, UniqueConstraint
from django.utils import timezone

from users.models import User


class Category(models.Model):
    """`Category` model."""

    namemaxlength = 256  # максимальная длина наименования категории
    name = models.CharField(max_length=namemaxlength)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(models.Model):
    """`Genre` model."""

    namemaxlength = 50  # максимальная длина наименования жанра
    name = models.CharField(max_length=namemaxlength)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """`Title` model."""

    name_max_length = 256  # максимальная длина названия произведения
    description_max_length = 2000  # максимальная длина описания произведения
    name = models.TextField(
        max_length=name_max_length,
        verbose_name='Название произведения',
    )
    description = models.TextField(
        max_length=description_max_length,
        verbose_name='Описание произведения',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        blank=True,
        null=True,
        verbose_name='Название категории',
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    year = models.PositiveIntegerField()

    @property
    def avg_score(self):
        return self.review_set.all().aggregate(Avg('score'))["score__avg"]
    rate = avg_score

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category', 'year'],
                name='%(app_label)s_%(class)s_unique_relationships',
            ),
        ]


class GenreTitle(models.Model):
    """Auxiliary class GenreTitle for many to many Genre and Title."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    verbose_name = 'жанр'


class Review(models.Model):
    """Класс отзывов."""

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата добавления обзора',
        # auto_now_add=True,
        db_index=True,
        default=timezone.now,
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='review_once')
        ]


class Comment(models.Model):
    """Класс комментариев."""

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария',
        # auto_now_add=True,
        db_index=True,
        default=timezone.now,
    )
