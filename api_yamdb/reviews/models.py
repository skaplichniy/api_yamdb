from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOISES = [
        (USER, 'USER'),
        (MODERATOR, 'MODERATOR'),
        (ADMIN, 'ADMIN')
    ]
    email = models.EmailField('E-mail', unique=True, max_length=254)
    username = models.CharField(
        'Имя пользователя', unique=True, max_length=150)
    bio = models.TextField('О себе', blank=True)
    role = models.CharField('Роль пользователя', max_length=10,
                            choices=ROLE_CHOISES, default=USER)
    confirmation_code = models.CharField(
        max_length=255,
        verbose_name='код авторизации',
        help_text='код')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    @property
    def is_user(self):
        return self.is_user

    @property
    def is_admin(self):
        return self.is_admin

    @property
    def is_moderator(self):
        return self.is_moderator


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='название')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        help_text='слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Наименование произведения',
        help_text='наименование', max_length=256, db_index=True,
    )
    year = models.IntegerField(
        verbose_name='Год произведения',
        validators=(validate_year, )
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='Описание',
        null=True,
        blank=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Муз. жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория произведения',
        db_index=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review (models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True,
        null=False,
        verbose_name='Произведение',
        help_text='Отзыв к произведению'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews', db_index=True,
        null=False, verbose_name='Автор',
        help_text='Автор отзыва'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.PositiveSmallIntegerField(
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
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывыы'


class Comments (models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Комментарий',
        help_text='Комментарий к отзыву')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария',
        help_text='Автор комментария')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
