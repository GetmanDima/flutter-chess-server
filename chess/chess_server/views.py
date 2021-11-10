# from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from .models import Application


@action(detail=True, methods=['get'], name='current_games')
def get_current_games(request):
    return HttpResponse('current games')


@action(detail=True, methods=['get'], name='current_games')
def get_last_games(request):
    return HttpResponse('last games')


@action(detail=True, methods=['get'], name='current_games')
def get_game(request):
    return HttpResponse('game')


class ApplicationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_applications(self, request):
        print(request.user.email)
        return HttpResponse('applications')

    @action(detail=True, methods=['post'])
    def create_application(self, request):
        application = Application.objects.create(author=request.user)
        return HttpResponse('create application')


@action(detail=True, methods=['delete'])
def delete_application(request, id):
    return HttpResponse('delete application')


class ApplicationAcceptView(ViewSet):
    @action(detail=True, methods=['post'])
    def accept_application(self, request, id):
        return HttpResponse('accept application')


class MoveView(ViewSet):
    @action(detail=True, methods=['post'])
    def get_moves(self, request):
        return HttpResponse('moves')
