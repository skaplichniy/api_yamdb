
from rest_framework import serializers
from reviews.models import Category, Genre, Titles, Review, Comments
from reviews.models import User
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Category


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    #genre = GenreField(slug_field='slug',
     #                  queryset=Genre.objects.all(), many=True)
    #category = CategoryField(slug_field='slug',
     #                        queryset=Category.objects.all(), required=True)
    #author = serializers.SlugRelatedField(
     #   slug_field='username',
      #  read_only=True
    #)
    #rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'

        def validate_year(self, value):
            if value > date.today().year:
                raise serializers.ValidationError(
                    'Год выпуска не может быть больше настоящего'
                )


class CurrentTitleDafault:
    requires_context = True

    def __call__(self, serializer_field):
        c_view = serializer_field.context['view']
        title_id = c_view.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        return title

    def __repr__(self):
        return '%s()' % self.__class__.__name__

class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Titles.objects.all(),
        required=False
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
        
    )
    
    class Meta:
        model = Review
        fields = '__all__'
      #  validators = (UniqueTogetherValidator(
       #     queryset=Review.objects.all(), fields=('title', 'author')),)

        def validate(self, data):
            if self.context['request'].method == 'POST':
                user = self.context['request'].user
                title_id = self.context['view'].kwargs.get('title_id')
                if Review.objects.filter(
                    author_id=user.id, title_id=title_id):
                    raise serializers.ValidationError(NOT_ALLOWED)
            return data


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('role',)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

