"""chess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chess_server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),

    path('applications/',
         views.ApplicationViewSet.as_view({'get': 'get_applications', 'post': 'create_application'}),
         name='applications'
         ),
    path('applications/<int:id>/',
         views.ApplicationDeleteView.as_view({'delete': 'delete_application'}),
         name='delete_application'
         ),
    path('applications/<int:id>/accept',
         views.ApplicationAcceptView.as_view({'post': 'accept_application'}),
         name='accept_application'
         ),
    path('applications/<int:id>/checkStatus',
         views.ApplicationCheckView.as_view({'get': 'check_application_status'}),
         name='check_application_status'
         ),

    path('games/current/', views.CurrentGamesView.as_view({'get': 'get_current_games'}), name='current_games'),
    path('games/last/', views.LastGamesView.as_view({'get': 'get_last_games'}), name='last_games'),
    path('games/<int:id>/', views.GameView.as_view({'get': 'get_game'}), name='get_game'),
    path('games/<int:game_id>/moves/',
         views.MoveView.as_view({'get': 'get_moves', 'post': 'create_move'}),
         name='applications'
         )
]

# from rest_framework import routers
# from chess_server import views
#
# router = routers.DefaultRouter()
# router.register('games/', views.GameViewSet, basename='games')
# urlpatterns = router.urls
