from django.contrib.auth.models import AbstractUser
from django.db import models


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
    confirmation_code = models.IntegerField(
        'Код подтверждения',
        max_length=6,
        null=True,
        blank=False,
    )

    def __str__(self):
        return self.email
