from django.contrib import admin
from .models import Application, Game, Move


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('author', 'color', 'time_mode', 'is_active', 'created_date')


class GameAdmin(admin.ModelAdmin):
    list_display = ('user_white', 'user_black', 'application', 'result', 'created_date')


class MoveAdmin(admin.ModelAdmin):
    list_display = ('game', 'fen', 'created_date')


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Move, MoveAdmin)
