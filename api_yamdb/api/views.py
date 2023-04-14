from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from users.permissions import IsUserWithPowerOrReadOnly
from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users.permissions import AdminOrReadOnly
from users.models import User


class TitleView(
    ListCreateAPIView,
):
    """
    Processing of the list `Title` objects.

    Endpoint `/api/v1/titles/`.
    """

    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = (
        'name',
        'year',
    )
    ordering = ('year',)
    filterset_class = TitleFilter
    permission_classes = (IsUserWithPowerOrReadOnly,)


class TitleViewDetail(
    RetrieveUpdateDestroyAPIView,
):
    """
    Processing of the single `Title` objects.

    Processing of endpoint `/api/v1/titles/<title_id>/`.
    """

    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def update(self, *args: list, **kwargs: dict):
        """
        Deny cccess to the PUT method .

        Args:
            *args: not used.
            **kwargs: not used.

        Returns:
            MethodNotAllowed exception.

        """
        raise MethodNotAllowed('PUT', detail='Use PATCH')

    def partial_update(
        self,
        request: HttpRequest,
        *args: list,
        **kwargs: dict,
    ):
        """
        Override Partial Update Code if desired.
        Args:
            request: HTTPRequest
            *args: not used
            **kwargs: not used

        Returns:
            Updated output.

        """
        return super().update(request, *args, **kwargs, partial=True)


class CategoryView(
    ListCreateAPIView,
):
    """
    Processing of the list `Category` objects.

    Endpoint `/api/v1/category/.
    """

    permission_classes = (AdminOrReadOnly,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewDetail(
    DestroyAPIView,
):
    """
    Processing of the single `Category` objects.

    Endpoint `/api/v1/category/<category_id>/`."""

    permission_classes = (AdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreView(
    ListCreateAPIView,
):
    """
    Processing of the list `Genre` objects.

    Endpoint `/api/v1/genre/`
    """

    permission_classes = (AdminOrReadOnly,)
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewDetail(
    DestroyAPIView,
):
    """
    Processing of the single `Genre` objects.

    Endpoint `/api/v1/genre/<genre_id>/`.
    """

    permission_classes = (AdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Список обзоров."""

    queryset = Review.objects.all().order_by('id')  # заглушка
    serializer_class = ReviewSerializer
    permission_classes = (IsUserWithPowerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            title=Title.objects.get(pk=self.kwargs.get('title_id')),
            author=User.objects.get(pk=self.request.user.id)
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Список комментариев."""

    serializer_class = CommentSerializer

    permission_classes = (IsUserWithPowerOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            review=review,
            author=User.objects.get(pk=self.request.user.id)
        )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()
