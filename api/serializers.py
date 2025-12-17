from rest_framework import serializers
from .models import CustomUser, Game, SquadRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'gamertag', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6} # [cite: 39]
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class SquadRequestSerializer(serializers.ModelSerializer):
    # Estas líneas NO son automáticas, debes escribirlas:
    gamertag = serializers.ReadOnlyField(source='creator.gamertag')
    creator_username = serializers.ReadOnlyField(source='creator.username') # <--- ESTA ES LA CLAVE
    game_name = serializers.ReadOnlyField(source='game.nombre')

    class Meta:
        model = SquadRequest
        fields = ['id', 'gamertag', 'creator_username', 'game_name', 'rank_required', 'description', 'mic_required', 'created_at']