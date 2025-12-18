#!/usr/bin/env python
import os
import django
import random
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import CustomUser, Game, SquadRequest

def run():
    print("--- Iniciando carga de datos de prueba ---")

    # 1. Crear Usuarios de prueba (Requisito 2.1)
    usuarios_data = [
        {"user": "Faker", "pass": "sktt1faker", "tag": "Faker#SKT"},
        {"user": "S1mple", "pass": "csgo123", "tag": "S1mple#NAVI"},
        {"user": "TenZ", "pass": "val123", "tag": "TenZ#SEN"},
    ]

    usuarios_creados = []
    for u in usuarios_data:
        user, created = CustomUser.objects.get_or_create(
            username=u["user"],
            email=f"{u['user'].lower()}@test.com",
            defaults={"gamertag": u["tag"]}
        )
        if created:
            user.set_password(u["pass"])
            user.save()
            print(f"✅ Usuario creado: {u['user']}")
        else:
            print(f"ℹ️ Usuario existente: {u['user']}")
        usuarios_creados.append(user)

    # 2. Verificar que existan juegos (Requisito 2.2-B)
    juegos = list(Game.objects.all())
    if not juegos:
        print("❌ Error: No hay juegos en la base de datos. Ejecuta primero seed_games.py")
        return

    # 3. Crear Anuncios (Squads) (Requisito 2.2-C)
    descripciones = [
        "Busco gente seria para subir a Inmortal, tengo micro.",
        "Duo para rankeds nocturnas, main support.",
        "Torneo de fin de semana, falta uno para completar equipo.",
        "Jugando chill para aprender nuevas rotaciones.",
        "Busco gente con buena onda, nada de toxicidad por favor."
    ]

    print("\nPublicando anuncios de prueba...")
    for i in range(10):  # Creamos 10 anuncios aleatorios
        user = random.choice(usuarios_creados)
        juego = random.choice(juegos)
        
        squad = SquadRequest.objects.create(
            creator=user,
            game=juego,
            rank_required=random.choice(["Plata", "Oro", "Platino", "Diamante"]),
            mic_required=random.choice([True, False]),
            description=random.choice(descripciones),
            created_at=timezone.now()
        )
        print(f"🚀 Publicado: {juego.nombre} por {user.username}")

    print("\n--- ¡Proceso finalizado! Ya tienes datos reales para mostrar ---")

if __name__ == '__main__':
    run()