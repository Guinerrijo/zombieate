
import pygame
from src.utils.constants import TILE_SIZE

class EnemyBase:
    def __init__(self, x, y, level, speed, health, score_value):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.speed = speed
        self.health = health
        self.score_value = score_value
        self.direction = "down"  # Dirección inicial
        self.moving = False
        
        # Animación
        self.animation_frame = 0
        self.animation_timer = 0
    
    def update(self, player, level):
        """Actualiza el estado del enemigo (a implementar en subclases)"""
        pass
    
    def take_damage(self):
        """Reduce la salud del enemigo"""
        self.health -= 1
    
    def get_collision_rect(self):
        """Devuelve el rectángulo de colisión del enemigo"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen):
        """Renderiza al enemigo en pantalla"""
        current_sprite = self.sprites[self.direction][self.animation_frame]
        screen.blit(current_sprite, (self.x, self.y)) 