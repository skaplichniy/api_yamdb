from django.db import models


class Category(models.Model):
    CHOICES_CATEGORY = (
        ('books', 'Книги'),
        ('movies', 'Фильмы'),
        ('music', 'Музыка'),
    )
    name = models.CharField(max_length=300, choices = CHOICES_CATEGORY)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    CHOICES_GENRE = (
        ('story', 'Сказка'),
        ('rock', 'Рок'),
        ('arthouse', 'Артхаус'),
    )
    name = models.CharField(max_length=300, choices = CHOICES_GENRE)
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
        'Дата добавления', auto_now_add=True
    )
    score = models.IntegerField( 
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )


class Comments (models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

