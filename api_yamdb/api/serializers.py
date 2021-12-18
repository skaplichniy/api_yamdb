from rest_framework import serializers, status
from reviews.models import Category, Genre, Title, Review, Comments
from reviews.models import User
from django.shortcuts import get_object_or_404


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
        model = Title


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        required=False
    )

    class Meta:
        model = Review
        read_only_fields = ('title_id',)
        fields = '__all__'

    def validate(self, data):
        data_kwargs = self.context['request'].parser_context['kwargs']

        if 'pk' in data_kwargs:
            return data

        title_id = data_kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if self.context['request'].user.reviews.filter(title=title).exists():
            raise serializers.ValidationError(
                detail='Ваш отзыв уже существует!',
                code=status.HTTP_400_BAD_REQUEST)
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'author', 'review_id', 'text', 'pub_date')


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


class TokenSerializer(UserSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
