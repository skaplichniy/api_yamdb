from django.contrib import admin
from .models import Comments, Genre, Category, Title, Review


class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('category',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'pub_date',
        'score',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
