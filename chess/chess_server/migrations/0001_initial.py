# Generated by Django 3.2.9 on 2021-12-20 01:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=5)),
                ('time_mode', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=None, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='chess_server.application')),
                ('user_black', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_black', to=settings.AUTH_USER_MODEL)),
                ('user_white', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_white', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fen', models.CharField(max_length=64)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='chess_server.game')),
            ],
        ),
    ]
