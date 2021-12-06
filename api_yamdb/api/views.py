from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from reviews.models import User
from .serializers import GetTokenSerializer, UserSerializer, UserMeSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = IsAdminUser
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get_or_create()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Регистрация в сервисе отзывов',
            f'Спасибо за регистрацию! Ваш код подтверждения: {confirmation_code}',
            request.data['email'])
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    user = User.objects.filter(username=request.data['username'])


@action(
    methods=['get', 'patch'],
    detail=False,
    permission_classes=[IsAuthenticated],
    serializer_class=UserMeSerializer)
def me(self, request):
    self.kwargs['username'] = request.user.username
    if self.request.method == 'PATCH':
        self.partial_update(request)
        request.user.refresh_from_db()
    serializer = self.get_serializer(request.user)
    return Response(serializer.data)
