from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esto habilita /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index_view, name='index'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/login/', MyTokenView.as_view()),  # ⭐ Mejorado para incluir user_id
    path('api/games/', GameListView.as_view()),
    path('api/squads/', SquadListCreateView.as_view()),
    path('api/squads/<int:pk>/', SquadDetailDeleteView.as_view(), name='squad-detail-delete'),
    path('api/stats/', StatsView.as_view(), name='stats'),  # ⭐ AGREGADO
]