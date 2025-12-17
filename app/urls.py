from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    RegisterView,
    GameListView,
    SquadListCreateView,
    SquadDeleteView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),

    path('games/', GameListView.as_view()),

    path('squads/', SquadListCreateView.as_view()),
    path('squads/<int:pk>/', SquadDeleteView.as_view()),
]