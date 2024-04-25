from django.urls import path
from core import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('players/', views.players_list_view, name='players_list'),
    path('player_position/', views.player_position_view, name='player_position'),
]