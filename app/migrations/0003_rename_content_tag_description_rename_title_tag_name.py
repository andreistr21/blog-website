# Generated by Django 4.1.3 on 2022-11-22 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_tag_post_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='content',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
    ]
