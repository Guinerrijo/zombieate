#!/usr/bin/env python3
"""
Script para crear sprites de emergencia cuando no se pueden cargar los SVG
"""
import os
import pygame
from src.utils.constants import TILE_SIZE

def create_directory_if_not_exists(directory):
    """Crea un directorio si no existe"""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def create_player_sprites():
    """Crea sprites del jugador"""
    create_directory_if_not_exists("assets/images")
    
    directions = ["up", "down", "left", "right"]
    
    for direction in directions:
        for frame in [1, 2]:
            filename = f"assets/images/player_{direction}_{frame}.png"
            
            # Crear superficie
            sprite = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            sprite.fill((255, 99, 71, 255))  # Color rojo-naranja para el jugador
            
            # Añadir detalles según dirección
            if direction == "up" or direction == "down":
                # Cabeza
                pygame.draw.circle(sprite, (255, 215, 0), (TILE_SIZE//2, TILE_SIZE//3), TILE_SIZE//6)
                
                # Ojos
                if direction == "down":
                    pygame.draw.circle(sprite, (0, 0, 0), (TILE_SIZE//2 - 2, TILE_SIZE//3 - 1), 1)
                    pygame.draw.circle(sprite, (0, 0, 0), (TILE_SIZE//2 + 2, TILE_SIZE//3 - 1), 1)
            
            # Guardar imagen
            pygame.image.save(sprite, filename)
            print(f"Creado: {filename}")

def create_zombie_sprites():
    """Crea sprites de zombies"""
    create_directory_if_not_exists("assets/images")
    
    directions = ["up", "down", "left", "right"]
    
    for direction in directions:
        for frame in [1, 2]:
            filename = f"assets/images/zombie_{direction}_{frame}.png"
            
            # Crear superficie
            sprite = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            sprite.fill((144, 238, 144, 255))  # Color verde claro para zombies
            
            # Añadir detalles según dirección
            if direction == "up" or direction == "down":
                # Ojos
                eye_color = (255, 0, 0)  # Rojo
                if direction == "down":
                    pygame.draw.circle(sprite, eye_color, (TILE_SIZE//2 - 4, TILE_SIZE//3), 2)
                    pygame.draw.circle(sprite, eye_color, (TILE_SIZE//2 + 4, TILE_SIZE//3), 2)
            
            # Guardar imagen
            pygame.image.save(sprite, filename)
            print(f"Creado: {filename}")

def create_mummy_sprites():
    """Crea sprites de momias"""
    create_directory_if_not_exists("assets/images")
    
    directions = ["up", "down", "left", "right"]
    
    for direction in directions:
        for frame in [1, 2]:
            filename = f"assets/images/mummy_{direction}_{frame}.png"
            
            # Crear superficie
            sprite = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            sprite.fill((245, 222, 179, 255))  # Color beige para momias
            
            # Añadir detalles según dirección
            if direction == "up" or direction == "down":
                # Ojos
                eye_color = (255, 0, 0)  # Rojo
                if direction == "down":
                    pygame.draw.circle(sprite, eye_color, (TILE_SIZE//2 - 4, TILE_SIZE//3), 2)
                    pygame.draw.circle(sprite, eye_color, (TILE_SIZE//2 + 4, TILE_SIZE//3), 2)
            
            # Vendas (líneas horizontales)
            for y in range(TILE_SIZE//4, TILE_SIZE, TILE_SIZE//4):
                pygame.draw.line(sprite, (255, 255, 240), (0, y), (TILE_SIZE, y), 2)
            
            # Guardar imagen
            pygame.image.save(sprite, filename)
            print(f"Creado: {filename}")

def create_tile_sprites():
    """Crea sprites de tiles"""
    create_directory_if_not_exists("assets/images")
    
    # Crear tile de suelo
    floor_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    floor_tile.fill((139, 115, 85))  # Marrón claro
    
    # Añadir textura al suelo
    for i in range(4):
        for j in range(4):
            pygame.draw.line(
                floor_tile, 
                (122, 99, 72), 
                (i*8, j*8), 
                (i*8+4, j*8+4), 
                1
            )
    
    # Guardar tile de suelo
    pygame.image.save(floor_tile, "assets/images/floor.png")
    print("Creado: assets/images/floor.png")
    
    # Crear tile de pared
    wall_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall_tile.fill((105, 105, 105))  # Gris
    
    # Añadir textura de ladrillos
    for i in range(4):
        pygame.draw.line(
            wall_tile, 
            (80, 80, 80), 
            (0, i*8), 
            (TILE_SIZE, i*8), 
            1
        )
    
    for i in range(4):
        for j in range(2):
            offset = 16 if i % 2 == 0 else 0
            pygame.draw.line(
                wall_tile, 
                (80, 80, 80), 
                (offset + j*32, i*8), 
                (offset + j*32, i*8+8), 
                1
            )
    
    # Guardar tile de pared
    pygame.image.save(wall_tile, "assets/images/wall.png")
    print("Creado: assets/images/wall.png")

def create_projectile_sprite():
    """Crea sprite del proyectil de agua"""
    create_directory_if_not_exists("assets/images")
    
    # Crear superficie
    sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
    sprite.fill((30, 144, 255, 192))  # Color azul semitransparente para el agua
    
    # Añadir brillo
    pygame.draw.circle(sprite, (135, 206, 250), (6, 6), 3)
    
    # Guardar imagen
    pygame.image.save(sprite, "assets/images/water_projectile.png")
    print("Creado: assets/images/water_projectile.png")

def main():
    """Función principal"""
    # Inicializar pygame
    pygame.init()
    
    # Crear sprites
    create_player_sprites()
    create_zombie_sprites()
    create_mummy_sprites()
    create_tile_sprites()
    create_projectile_sprite()
    
    print("Sprites creados con éxito")

if __name__ == "__main__":
    main() 