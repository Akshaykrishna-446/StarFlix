# Generated by Django 5.0.4 on 2024-04-22 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0008_episode_tvshow_epi_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movies',
            old_name='movie_genre',
            new_name='movie_genres',
        ),
    ]
