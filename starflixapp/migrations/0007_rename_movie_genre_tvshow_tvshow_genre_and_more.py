# Generated by Django 5.0.4 on 2024-04-21 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0006_genre_season_remove_movies_movie_genres_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tvshow',
            old_name='movie_genre',
            new_name='TVShow_genre',
        ),
        migrations.RenameField(
            model_name='tvshow',
            old_name='movie_image',
            new_name='TVShow_image',
        ),
        migrations.RenameField(
            model_name='tvshow',
            old_name='movie_thumbnail',
            new_name='TVShow_thumbnail',
        ),
    ]
