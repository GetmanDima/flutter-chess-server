from django.db.models import Q
from django.forms import model_to_dict
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Application, Game, Move


class CurrentGamesView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_current_games(self, request):
        games = Game.objects\
            .filter(Q(user_white=request.user) | Q(user_black=request.user), result=None)\
            .all()\
            .values()
        return Response({'games': games})


class LastGamesView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_last_games(self, request):
        games = Game.objects\
            .filter(Q(user_white=request.user) | Q(user_black=request.user), ~Q(result=None))\
            .all()\
            .values()
        return Response({'games': games})


class GameView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_game(self, request, id):
        game = model_to_dict(Game.objects.get(id=id))
        return Response({"game": game})


class ApplicationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_applications(self, request):
        applications = Application.objects.all().values()
        return Response({"applications": applications})

    @action(detail=True, methods=['post'])
    def create_application(self, request):
        Application.objects.create(author=request.user, color=request.POST.get('color'))
        return Response(status=201)


class ApplicationDeleteView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['delete'])
    def delete_application(self, request, id):
        Application.objects.filter(id=id).delete()
        return Response(status=204)


class ApplicationAcceptView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def accept_application(self, request, id):
        application = Application.objects.get(id=id)

        if not application.is_active:
            return Response({'accept': False})

        user_white = application.author if application.color == 'white' else request.user
        user_black = application.author if application.color == 'black' else request.user

        application.is_active = False
        application.save()

        game = model_to_dict(
            Game.objects.create(
                user_white=user_white,
                user_black=user_black,
                application=application
            )
        )

        return Response({'accept': True, 'game': game})


class ApplicationCheckView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def check_application_status(self, request, id):
        application = Application.objects.get(id=id)

        if application.is_active:
            return Response({"application_status": application.is_active})

        game = model_to_dict(Game.objects.filter(application=application).first())

        return Response(
            {
                "application_status": application.is_active,
                "game": game
            }
        )


class MoveView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_moves(self, request, game_id):
        moves = Move.objects\
            .filter(id__gt=int(request.GET.get('lastMoveId')), game_id=game_id)\
            .all()\
            .values()
        return Response({'moves': moves})

    @action(detail=True, methods=['post'])
    def create_move(self, request, game_id):
        moves = Move.objects.create(fen=request.POST.get('fen'), game_id=game_id)
        return Response(status=201)
