# Generated by Django 5.0.4 on 2024-05-01 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0014_alter_episode_season_alter_season_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='trendingORpriority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='trendingORpriority',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='FavouriteTV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tv_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='starflixapp.episode')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.user_reg')),
            ],
        ),
        migrations.CreateModel(
            name='WatchlistTV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tv_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='starflixapp.episode')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.user_reg')),
            ],
        ),
    ]
