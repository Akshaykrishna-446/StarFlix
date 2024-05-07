# Generated by Django 5.0.4 on 2024-05-07 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starflixapp', '0025_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='TVReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('episode_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.episode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starflixapp.user_reg')),
            ],
        ),
    ]