from random import choice
from string import ascii_letters

from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsAdminUser
from users.serializers import (
    AdminSerializer,
    CustomUserSerializer,
    RegistrationSerializer,
    TokenObtainSerializer,
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_token_for_user(request):
    serializer = TokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(username=request.data.get('username'))
            if user.username == request.data.get(
                'username',
            ) and user.confirmation_code == request.data.get(
                'confirmation_code',
            ):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'token': str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response(
                'Username not exsist',
                status=status.HTTP_404_NOT_FOUND,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = "".join([choice(ascii_letters) for i in range(10)])
        try:
            user, created = User.objects.get_or_create(
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                'Take your token',
                confirmation_code,
                'from@example.com',
                [request.data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(
                'Username or email has already taken',
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def user_me_info(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.data)
