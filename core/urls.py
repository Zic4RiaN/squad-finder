from django.contrib import admin
from django.urls import path
from api.views import (
    index_view, dashboard_view, # Vistas de Template
    RegisterView, GameListView, SquadListCreateView, SquadDeleteView # Vistas API
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rutas de Navegación (HTML)
    path('', index_view, name='index'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # 2. Rutas de la API (JSON)
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/games/', GameListView.as_view()),
    path('api/squads/', SquadListCreateView.as_view()),
    path('api/squads/<int:pk>/', SquadDeleteView.as_view()),
]