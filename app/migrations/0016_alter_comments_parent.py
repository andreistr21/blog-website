# Generated by Django 4.1.3 on 2023-01-12 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_comments_email_remove_comments_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.comments'),
        ),
    ]