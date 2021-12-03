from rest_framework import serializers
from yamdb.models import Category, Genre, Titles


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    category = CategorySerializer()

    class Meta:
        model = Titles
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

