from rest_framework import serializers
from .models import CustomUser, Game, SquadRequest

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'gamertag')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            gamertag=validated_data['gamertag'],
            password=validated_data['password']
        )
        return user

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class SquadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.gamertag', read_only=True)
    game = serializers.CharField(source='game.name', read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(),
        write_only=True,
        source='game'
    )

    class Meta:
        model = SquadRequest
        fields = (
            'id',
            'user',
            'game',
            'game_id',
            'rank_required',
            'mic_required',
            'description',
            'created_at'
        )

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Mínimo 10 caracteres.")
        return value