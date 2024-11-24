# Generated by Django 4.1.1 on 2024-11-21 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewer', '0006_movie_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=None)),
                ('text', models.TextField(default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.movie')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
