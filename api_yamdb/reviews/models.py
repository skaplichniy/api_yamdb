from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOISES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Пользовательская роль',
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True,
        blank=False,
    )

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

class Titles(models.Model):
    name = models.CharField(max_length=300)
    genre = models.ForeignKey(Genre)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        help_text='Категория произведения',
        verbose_name='Категория')
    slug = models.SlugField(null=False, unique=True)
    description = models.CharField(max_length=1000, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review (models.Model):
    title_id = models.OneToOneField(
        Titles, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField( 
        'оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('title_id', 'author', ), name='unique pair'), )


class Comments (models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
