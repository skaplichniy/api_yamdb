
from rest_framework import serializers
from reviews.models import Category, Genre, Titles, Review, Comments
from reviews.models import User
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from rest_framework import status
import datetime as dt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class ReadTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title_id=obj.id
        ).aggregate(Avg('score'))
        return rating['score__avg']

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'rating', 'category', 'genre')
        model = Titles


class WriteTitleSerializer(ReadTitleSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

class TitleDafault:
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context['view']
        title_id = view.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        return title

    def __repr__(self):
        return '%s()' % self.__class__.__name__

class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.HiddenField(
        default=TitleDafault()
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
        
    )
    
    class Meta:
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Хватит! Ты уже оставил отзыв!'
            )
        ]
      

        #def validate(self, data):
         #   if self.context['request'].method == 'POST':
          #      user = self.context['request'].user
           #     title_id = self.context['view'].kwargs.get('title_id')
            #    if Review.objects.filter(
             #       author_id=user.id, title_id=title_id):
              #      raise serializers.ValidationError('может быть только один отзыв')
           # return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comments


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('role',)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()