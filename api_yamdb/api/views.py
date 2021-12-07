
from rest_framework import permissions, viewsets
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer
from .serializers import ReviewSerializer, CommentsSerializer
from reviews.models import Category, Genre, Titles, Review
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from .permissions import AuthorOrModeratorOrAdminOrReadonly, AdminOrReadonly
from reviews.models import User
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from .serializers import GetTokenSerializer, UserSerializer, UserMeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadonly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadonly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadonly,)
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrModeratorOrAdminOrReadonly,)
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('post_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('post_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


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

