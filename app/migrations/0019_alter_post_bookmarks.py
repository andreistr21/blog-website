# Generated by Django 4.1.3 on 2023-01-13 17:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_post_bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
