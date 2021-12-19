import uuid

from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.models import Category, Genre, Title, Review, User

from .filter import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleWriteSerializer, TitleReadSerializer,
                          SignupSerializer, ReviewSerializer,
                          CommentsSerializer, TokenSerializer, UserSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrModerator, )
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(
        methods=('get', 'patch'), detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def code(request):
    email = request.data['email']
    username = email.split('@')[0]
    user = User.objects.create(
        username=username,
        email=email,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code',
        f'{confirmation_code}',
        f'{settings.ADMIN_EMAIL}',
        [f'{email}'],
        fail_silently=False,
    )
    return Response(confirmation_code, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
    return JsonResponse(
        {'status': 'false', 'message': 'Что-то пошло не так'}, status=400,
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
    user, created = User.objects.get_or_create(
        **serializer.validated_data,
        confirmation_code=confirmation_code
    )
    send_mail(
        subject=settings.EMAIL_BACKEND,
        message=user.confirmation_code,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(email,))
    return Response(serializer.data, status=status.HTTP_200_OK)
