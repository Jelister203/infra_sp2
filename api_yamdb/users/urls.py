"""Определяет схемы URL для пользователей."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, api_registration, api_token_for_user

app_name = 'users'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', api_registration, name='api_registration'),
    path('v1/auth/token/', api_token_for_user, name='api_token_for_user'),
    path('v1/', include(router.urls)),
]
