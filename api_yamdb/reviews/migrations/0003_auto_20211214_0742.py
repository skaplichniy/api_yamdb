# Generated by Django 3.0 on 2021-12-14 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20211214_0729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='code',
            new_name='confirmation_code',
        ),
    ]
