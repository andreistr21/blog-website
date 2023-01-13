# Generated by Django 4.1.3 on 2023-01-13 16:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_alter_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
