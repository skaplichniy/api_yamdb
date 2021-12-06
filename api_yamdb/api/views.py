from rest_framework import permissions, viewsets
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer
from .serializers import ReviewSerializer, CommentsSerializer
from reviews.models import Category, Genre, Titles, Review, Comments
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User
from .serializers import UserSerializer
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


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


# class UserViewSet(viewsets.ModelViewSet):
  #  queryset = User.objects.all()
  #  serializer_class = UserSerializer
  #  lookup_field = 'username'

   # @api_view(['POST'])
   # def signup(request):
    
   # @api_view(['POST'])
   # def get_token(request):
