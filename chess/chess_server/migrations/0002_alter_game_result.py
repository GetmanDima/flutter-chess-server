# Generated by Django 3.2.9 on 2021-11-10 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='result',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
