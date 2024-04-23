# Generated by Django 5.0.4 on 2024-04-20 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0004_movies_movie_mon_yr'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='ageGroup',
            field=models.TextField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='movies',
            name='movie_duration',
            field=models.TextField(max_length=5),
        ),
        migrations.AlterField(
            model_name='movies',
            name='movie_genres',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='movies',
            name='movie_mon_yr',
            field=models.TextField(max_length=30, null=True),
        ),
    ]