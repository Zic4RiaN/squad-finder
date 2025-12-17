
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Game, SquadRequest
from .serializers import (
    RegisterSerializer,
    GameSerializer,
    SquadSerializer
)
from .permissions import IsOwner

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario creado correctamente"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

class SquadListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        squads = SquadRequest.objects.all().order_by('-created_at')

        game_slug = request.query_params.get('game_slug')
        if game_slug:
            squads = squads.filter(game__slug=game_slug)

        serializer = SquadSerializer(squads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SquadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SquadDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        squad = SquadRequest.objects.get(pk=pk)
        self.check_object_permissions(request, squad)
        squad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
