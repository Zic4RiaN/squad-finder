from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, Game, SquadRequest
from .serializers import UserSerializer, GameSerializer, SquadRequestSerializer
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

# --- VISTAS DE NAVEGACIÓN (FRONTEND) ---

def index_view(request):
    """Renderiza la página de inicio (Login/Registro)."""
    return render(request, 'index.html')

def dashboard_view(request):
    """Renderiza el muro principal donde se ven los squads."""
    return render(request, 'dashboard.html')


# --- VISTAS DE LA API (BACKEND) ---

# 1. AUTENTICACIÓN PERSONALIZADA (Para que el Login devuelva el ID)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenSerializer(TokenObtainPairSerializer):
    """Añade datos extra al token para que el JS sepa quién es el usuario."""
    def validate(self, attrs):
        data = super().validate(attrs)
        # Esto es lo que permite que el JS guarde 'my_id' y 'current_user'
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data

class MyTokenView(TokenObtainPairView):
    """Vista para obtener el Token (reemplaza la de defecto)."""
    serializer_class = MyTokenSerializer


# 2. REGISTRO Y JUEGOS
class RegisterView(generics.CreateAPIView):
    """Permite crear nuevos usuarios (Público)."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class GameListView(generics.ListAPIView):
    """Lista todos los juegos disponibles (Público)."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]


# 3. GESTIÓN DE SQUADS (Muro y Borrado)
class SquadListCreateView(generics.ListCreateAPIView):
    """Lista todos los squads o crea uno nuevo (Requiere Token)."""
    queryset = SquadRequest.objects.all()
    serializer_class = SquadRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna automáticamente al usuario logueado como creador
        serializer.save(creator=self.request.user)

class SquadDetailDeleteView(generics.RetrieveDestroyAPIView):
    """Maneja las 2 funciones: Ver detalle (GET) y Eliminar (DELETE)."""
    queryset = SquadRequest.objects.all()
    serializer_class = SquadRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # SEGURIDAD: Solo el dueño del post puede borrarlo
        if instance.creator != self.request.user:
            raise PermissionDenied("No tienes permiso para borrar este anuncio.")
        instance.delete()


# 4. ESTADÍSTICAS DEL DASHBOARD
class StatsView(APIView):
    """Devuelve los contadores para las tarjetas superiores del dashboard."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            "squads_total": SquadRequest.objects.count(),
            "usuarios": CustomUser.objects.count(),
            "squads_hoy": SquadRequest.objects.filter(created_at__date=timezone.now().date()).count()
        })