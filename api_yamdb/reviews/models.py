from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.core.exceptions import ValidationError


class UserRole(models.TextChoices):
    ADMIN = "admin", "Администратор"
    MODERATOR = "moderator", "Модератор"
    USER = "user", "Пользователь"


class User(AbstractUser):
    email = models.EmailField('E-mail', unique=True, max_length=254)
    username = models.CharField('Имя пользователя', unique=True, max_length=150)
    bio = models.TextField("О себе", blank=True)
    role = models.CharField("Роль пользователя", max_length=10,
                            choices=UserRole.choices, default=UserRole.USER)
    confirmation_code = models.CharField(max_length=255)

    class Meta:
        ordering = ("username",)


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Titles(models.Model):
    def year_validator(value):
        if value > datetime.date.today().year:
            raise ValidationError(
                ('%(value)s год не должен быть больше нынешнего!'),
                params={'value': value},
            )

    name = models.CharField(
        verbose_name='Наименование произведения',
        max_length=256, db_index=True,
    )
    year = models.IntegerField(verbose_name='Год произведения',
                               validators=[year_validator],)
    description = models.TextField(verbose_name='Описание произведения',
                                   null=True, blank=True,)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        db_index=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review (models.Model):
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews', db_index=True,
        null=False
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews', db_index=True,
        null=False
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('title', 'author', ), name='unique pair'), )


class Comments (models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
