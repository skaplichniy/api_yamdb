from django.shortcuts import render
from rest_framework import permissions, viewsets
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer
from yamdb.models import Category, Genre, Titles

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

