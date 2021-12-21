import datetime
from time import timezone

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
        user_fields = ['id', 'username', 'first_name', 'last_name']
        full_games = []
        games = Game.objects \
            .filter(Q(user_white=request.user) | Q(user_black=request.user), result=None) \
            .all()

        for game in games:
            full_game = model_to_dict(game)
            full_game['user_white'] = \
                model_to_dict(game.user_white, fields=user_fields)
            full_game['user_black'] = \
                model_to_dict(game.user_black, fields=user_fields)
            full_game['application'] = \
                model_to_dict(game.application)
            full_game['application']['author'] = \
                model_to_dict(game.application.author, fields=user_fields)

            full_games.append(full_game)

        return Response({'games': full_games})


class LastGamesView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_last_games(self, request):
        user_fields = ['id', 'username', 'first_name', 'last_name']
        full_games = []
        games = Game.objects\
            .filter(Q(user_white=request.user) | Q(user_black=request.user), ~Q(result=None))\
            .all()

        for game in games:
            full_game = model_to_dict(game)
            full_game['user_white'] = \
                model_to_dict(game.user_white, fields=user_fields)
            full_game['user_black'] = \
                model_to_dict(game.user_black, fields=user_fields)
            full_game['application'] = \
                model_to_dict(game.application)
            full_game['application']['author'] = \
                model_to_dict(game.application.author, fields=user_fields)

            full_games.append(full_game)

        return Response({'games': full_games})


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
        is_personal = request.GET.__contains__('personal')

        applications_with_authors = []

        if is_personal:
            applications = Application.objects.filter(is_active=True, author=request.user).all()
        else:
            print('non')
            applications = Application.objects.filter(is_active=True).all()

        for application in applications:
            application_with_user = model_to_dict(application)
            application_with_user['author'] = \
                model_to_dict(application.author, fields=['id', 'username', 'first_name', 'last_name'])

            applications_with_authors.append(application_with_user)

        return Response({"applications": applications_with_authors})

    @action(detail=True, methods=['post'])
    def create_application(self, request):
        Application.objects.create(
            author=request.user,
            color=request.POST.get('color'),
            time_mode=request.POST.get('timeMode')
        )
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
        user_fields = ['id', 'username', 'first_name', 'last_name']
        full_game = game
        full_game['user_white'] = model_to_dict(user_white, fields=user_fields)
        full_game['user_black'] = model_to_dict(user_black, fields=user_fields)
        full_game['application'] = model_to_dict(application)
        full_game['application']['author'] = model_to_dict(application.author, fields=user_fields)

        return Response({'accept': True, 'game': full_game})


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
        last_move_id = request.GET.get('lastMoveId') or '0'

        moves = Move.objects\
            .filter(id__gt=int(last_move_id), game_id=game_id)\
            .all()

        game = Game.objects.get(id=game_id)
        time_arr = game.application.time_mode.split(" + ")
        white_time = int(time_arr[0]) * 60
        black_time = int(time_arr[0]) * 60

        if len(moves) > 1:
            white_first_move = moves[0]
            black_first_move = moves[1]

            if len(moves) % 2 == 0:
                white_last_time = datetime.datetime.now(datetime.timezone.utc)
                black_last_time = moves[len(moves) - 2].created_date
            else:
                white_last_time = moves[len(moves) - 2].created_date
                black_last_time = datetime.datetime.now(datetime.timezone.utc)
            print(int((white_last_time - white_first_move.created_date).total_seconds()))
            white_time -= int((white_last_time - white_first_move.created_date).total_seconds())
            black_time -= int((black_last_time - black_first_move.created_date).total_seconds())
        print('dsfdfs')
        return Response(
            {
                'moves': moves.values(),
                "whiteTime": max(0, white_time),
                "blackTime": max(0, black_time),
                "result": game.result
            }
        )

    @action(detail=True, methods=['post'])
    def create_move(self, request, game_id):
        new_move = Move.objects.create(
            fen=request.POST.get('fen'),
            game_id=game_id
        )

        moves = Move.objects \
            .filter(game_id=game_id) \
            .all()

        game = Game.objects.get(id=game_id)
        time_arr = game.application.time_mode.split(" + ")
        white_time = int(time_arr[0]) * 60
        black_time = int(time_arr[0]) * 60

        if len(moves) > 1:
            white_first_move = moves[0]
            black_first_move = moves[1]

            if len(moves) % 2 == 0:
                white_last_move = moves[len(moves) - 1]
                black_last_move = moves[len(moves) - 2]
            else:
                white_last_move = moves[len(moves) - 2]
                black_last_move = moves[len(moves) - 1]

            white_time -= int((white_last_move.created_date - white_first_move.created_date).total_seconds())
            black_time -= int((black_last_move.created_date - black_first_move.created_date).total_seconds())

        return Response(
            {
                'whiteTime': max(0, white_time),
                'blackTime': max(0, black_time)
            },
            status=201
        )


class UserView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def get_auth_user(self, request):
        user_fields = ['id', 'username', 'first_name', 'last_name']
        return Response({"user": model_to_dict(request.user, fields=user_fields)})
