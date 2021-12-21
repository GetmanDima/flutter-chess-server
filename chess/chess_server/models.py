from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Application(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    color = models.CharField(max_length=5)
    time_mode = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)


class Game(models.Model):
    user_white = models.ForeignKey(User, related_name='user_white', on_delete=models.CASCADE)
    user_black = models.ForeignKey(User, related_name='user_black', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='application', on_delete=models.CASCADE)
    result = models.IntegerField(default=None, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    fen = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)
