# Generated by Django 5.0.4 on 2024-04-23 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0010_movies_trendingorpriority_tvshow_trendingorpriority'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvshow',
            name='howmanyseasons',
            field=models.IntegerField(null=True),
        ),
    ]