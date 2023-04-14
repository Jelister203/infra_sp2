from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryView,
    CategoryViewDetail,
    CommentViewSet,
    GenreView,
    GenreViewDetail,
    ReviewViewSet,
    TitleView,
    TitleViewDetail,
)
from users.views import CustomUserViewSet, api_registration, api_token_for_user

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register(r'users/<int:id>/', CustomUserViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register(
    (
        r'^titles/(?P<title_id>\d+)'
        + r'/reviews/(?P<review_id>\d+)'
        + r'/comments/(?P<comment_id>\d+)'
    ),
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('auth/signup/', api_registration, name='api_registration'),
    path('auth/token/', api_token_for_user, name='api_token_for_user'),
    path('genres/', GenreView.as_view()),
    path('genres/<slug:slug>/', GenreViewDetail.as_view()),
    path('categories/', CategoryView.as_view()),
    path('categories/<slug:slug>/', CategoryViewDetail.as_view()),
    path('titles/', TitleView.as_view()),
    path('titles/<int:pk>/', TitleViewDetail.as_view()),
]
urlpatterns += router.urls
