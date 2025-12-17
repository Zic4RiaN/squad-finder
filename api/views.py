from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomUser, Game, SquadRequest
from .serializers import UserSerializer, GameSerializer, SquadRequestSerializer
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.exceptions import PermissionDenied

def index_view(request):
    """Renderiza la página principal (Login/Registro)"""
    return render(request, 'index.html')

def dashboard_view(request):
    """Renderiza el muro de squads y reportes"""
    return render(request, 'dashboard.html')

# A. Registro de Usuario [cite: 37]
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# B. Juegos (Público) [cite: 44, 47]
class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    # REQUISITO CUMPLIDO: Cualquiera puede ver, no pide Token
    permission_classes = [permissions.AllowAny]

# C. Squads (Listar y Crear) [cite: 48]
class SquadListCreateView(generics.ListCreateAPIView):
    queryset = SquadRequest.objects.all()
    serializer_class = SquadRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Esto guarda al usuario logueado como el dueño
        serializer.save(creator=self.request.user)

# D. Borrar Anuncio (Permiso Custom) [cite: 63, 66]
class SquadDeleteView(generics.DestroyAPIView):
    queryset = SquadRequest.objects.all()
    serializer_class = SquadRequestSerializer
    permission_classes = [permissions.IsAuthenticated] # [cite: 60]

    def perform_destroy(self, instance):
        # Lógica: Solo el dueño puede borrar [cite: 66]
        if instance.creator != self.request.user:
            raise PermissionDenied("No tienes permiso para borrar este anuncio.") # Retorna 403 [cite: 67]
        instance.delete()