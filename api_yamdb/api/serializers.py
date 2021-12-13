
from rest_framework import serializers
from reviews.models import Category, Genre, Titles, Review, Comments
from reviews.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': True}
        }
        lookup_field = 'username'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        

class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
        model = Titles


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
       # default=serializers.CurrentUserDefault()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            # return data

            user = self.context['view'].kwargs.get('title_id')
            title_id = self.context['request'].user
            if Review.objects.filter(
                    author=user, title=title_id).exists():
                raise serializers.ValidationError(
                     'Вы уже написали отзыв к этому произведению.'
                )
            return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value

    class Meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        exclude = ['review']


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError('Имя занято')
        return name

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError('Юзернейм занят')
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError('Почта занята')
        return data
