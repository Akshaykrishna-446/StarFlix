# Generated by Django 5.0.4 on 2024-05-03 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0017_lastplayed'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastplayedMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.movies')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.user_reg')),
            ],
        ),
        migrations.CreateModel(
            name='LastplayedTV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epi_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.episode')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.user_reg')),
            ],
        ),
        migrations.DeleteModel(
            name='Lastplayed',
        ),
    ]