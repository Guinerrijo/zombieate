# HUD (Heads-Up Display) del juego
# Autor: [Tu Nombre] - [Tu Matrícula]

import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, GREEN
from src.utils.image_loader import load_image, create_fallback_surface
import os

class HUD:
    """Clase para mostrar información en pantalla durante el juego"""
    def __init__(self, game):
        self.game = game
        
        # Cargar ícono de salud
        health_png = "assets/images/health_icon.png"
        health_svg = "assets/images/health_icon.svg"
        
        if os.path.exists(health_png):
            self.health_icon = load_image(health_png, (24, 24))
        elif os.path.exists(health_svg):
            self.health_icon = load_image(health_svg, (24, 24))
        else:
            print("No se encontró imagen para el ícono de salud, usando respaldo")
            self.health_icon = self.create_health_icon()
        
        # Fuentes
        self.font = pygame.font.Font(None, 36)
    
    def create_health_icon(self):
        """Crea un ícono de salud (corazón)"""
        icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        
        # Dibujar un corazón rojo
        pygame.draw.polygon(icon, RED, [
            (12, 6), (9, 3), (3, 6), (3, 12), 
            (12, 21), (21, 12), (21, 6), (15, 3)
        ])
        
        return icon
    
    def render(self, screen):
        """Renderiza el HUD en pantalla"""
        # Mostrar puntuación
        score_text = self.font.render(f"Puntuación: {self.game.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Mostrar salud
        for i in range(self.game.player.health):
            screen.blit(self.health_icon, (SCREEN_WIDTH - 40 - i * 30, 10))
        
        # Mostrar número de enemigos restantes
        enemies_text = self.font.render(f"Enemigos: {len(self.game.enemies)}", True, WHITE)
        screen.blit(enemies_text, (10, 50)) 