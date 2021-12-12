from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'

class Titles(models.Model):
    name = models.CharField(max_length=300)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр'
    )
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
