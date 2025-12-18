from django.urls import path
from .views import (
    SquadListCreateView, 
    SquadDetailView,  # <--- Importante
    SquadDeleteView, 
    StatsView
)

urlpatterns = [
    path('api/squads/', SquadListCreateView.as_view(), name='squad-list'),
    
    # Esta línea permite que el mismo ID sirva para VER (GET) y BORRAR (DELETE)
    # Django Rest Framework se encarga de dirigir el tráfico según el método
    path('api/squads/<int:pk>/', SquadDetailView.as_view(), name='squad-detail'), 
    
    # Si prefieres rutas separadas para no confundirte, usa esta:
    path('api/squads/delete/<int:pk>/', SquadDeleteView.as_view(), name='squad-delete'),

    path('api/stats/', StatsView.as_view(), name='stats'),
]