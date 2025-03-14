# Cargador de niveles
# Autor: [Tu Nombre] - [Tu Matrícula]

import pygame
from src.utils.constants import TILE_SIZE

class Level:
    """Clase que representa un nivel del juego"""
    def __init__(self, width, height, tile_map, player_start, zombie_starts, mummy_starts):
        self.width = width
        self.height = height
        self.tile_map = tile_map
        self.player_start = player_start
        self.zombie_starts = zombie_starts
        self.mummy_starts = mummy_starts
        
        # Cargar imágenes de tiles
        self.load_tiles()
    
    def load_tiles(self):
        """Carga las imágenes de los tiles"""
        self.tiles = {
            0: pygame.image.load("assets/images/floor.svg"),  # Suelo
            1: pygame.image.load("assets/images/wall.svg"),   # Pared
            2: pygame.image.load("assets/images/bush.svg"),   # Arbusto
            3: pygame.image.load("assets/images/water.svg")   # Agua
        }
        
        # Escalar tiles
        for key in self.tiles:
            self.tiles[key] = pygame.transform.scale(self.tiles[key], (TILE_SIZE, TILE_SIZE))
    
    def is_collision(self, x, y, width, height):
        """Comprueba si hay colisión en las coordenadas dadas"""
        # Convertir coordenadas de píxeles a coordenadas de tiles
        tile_x1 = int(x / TILE_SIZE)
        tile_y1 = int(y / TILE_SIZE)
        tile_x2 = int((x + width - 1) / TILE_SIZE)
        tile_y2 = int((y + height - 1) / TILE_SIZE)
        
        # Comprobar cada tile en el área
        for ty in range(tile_y1, tile_y2 + 1):
            for tx in range(tile_x1, tile_x2 + 1):
                if self.is_tile_blocked(tx, ty):
                    return True
        
        return False
    
    def is_tile_blocked(self, tx, ty):
        """Comprueba si un tile es un obstáculo"""
        # Comprobar límites del mapa
        if tx < 0 or tx >= self.width or ty < 0 or ty >= self.height:
            return True
        
        # Comprobar tipo de tile (0 es suelo, el resto son obstáculos)
        return self.tile_map[ty][tx] != 0
    
    def get_player_start(self):
        """Devuelve la posición inicial del jugador"""
        return self.player_start
    
    def get_zombie_starts(self):
        """Devuelve las posiciones iniciales de los zombies"""
        return self.zombie_starts
    
    def get_mummy_starts(self):
        """Devuelve las posiciones iniciales de las momias"""
        return self.mummy_starts
    
    def render(self, screen):
        """Renderiza el nivel en pantalla"""
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.tile_map[y][x]
                screen.blit(self.tiles[tile_type], (x * TILE_SIZE, y * TILE_SIZE))

class LevelLoader:
    """Clase para cargar niveles"""
    def __init__(self):
        # Definir niveles predefinidos
        self.levels = [
            self.create_level_1(),
            self.create_level_2(),
            self.create_level_3()
        ]
    
    def load_level(self, level_number):
        """Carga un nivel por su número"""
        if 1 <= level_number <= len(self.levels):
            return self.levels[level_number - 1]
        else:
            # Si el nivel no existe, devolver el primer nivel
            return self.levels[0]
    
    def create_level_1(self):
        """Crea el primer nivel"""
        width = 25
        height = 20
        
        # Crear mapa de tiles (0: suelo, 1: pared, 2: arbusto, 3: agua)
        tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Posición inicial del jugador
        player_start = (TILE_SIZE * 12, TILE_SIZE * 15)
        
        # Posiciones iniciales de los zombies
        zombie_starts = [
            (TILE_SIZE * 5, TILE_SIZE * 5),
            (TILE_SIZE * 20, TILE_SIZE * 5),
            (TILE_SIZE * 5, TILE_SIZE * 15),
            (TILE_SIZE * 20, TILE_SIZE * 15)
        ]
        
        # Posiciones iniciales de las momias
        mummy_starts = [
            (TILE_SIZE * 12, TILE_SIZE * 5)
        ]
        
        return Level(width, height, tile_map, player_start, zombie_starts, mummy_starts)
    
    def create_level_2(self):
        """Crea el segundo nivel"""
        width = 25
        height = 20
        
        # Crear mapa de tiles (0: suelo, 1: pared, 2: arbusto, 3: agua)
        tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Posición inicial del jugador
        player_start = (TILE_SIZE * 12, TILE_SIZE * 10)
        
        # Posiciones iniciales de los zombies
        zombie_starts = [
            (TILE_SIZE * 3, TILE_SIZE * 3),
            (TILE_SIZE * 3, TILE_SIZE * 16),
            (TILE_SIZE * 21, TILE_SIZE * 3),
            (TILE_SIZE * 21, TILE_SIZE * 16),
            (TILE_SIZE * 12, TILE_SIZE * 3),
            (TILE_SIZE * 12, TILE_SIZE * 16)
        ]
        
        # Posiciones iniciales de las momias
        mummy_starts = [
            (TILE_SIZE * 3, TILE_SIZE * 10),
            (TILE_SIZE * 21, TILE_SIZE * 10)
        ]
        
        return Level(width, height, tile_map, player_start, zombie_starts, mummy_starts)
    
    def create_level_3(self):
        """Crea el tercer nivel"""
        width = 25
        height = 20
        
        # Crear mapa de tiles (0: suelo, 1: pared, 2: arbusto, 3: agua)
        tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Posición inicial del jugador
        player_start = (TILE_SIZE * 12, TILE_SIZE * 10)
        
        # Posiciones iniciales de los zombies
        zombie_starts = [
            (TILE_SIZE * 3, TILE_SIZE * 3),
            (TILE_SIZE * 21, TILE_SIZE * 3),
            (TILE_SIZE * 3, TILE_SIZE * 16),
            (TILE_SIZE * 21, TILE_SIZE * 16),
            (TILE_SIZE * 12, TILE_SIZE * 3),
            (TILE_SIZE * 12, TILE_SIZE * 16),
            (TILE_SIZE * 3, TILE_SIZE * 10),
            (TILE_SIZE * 21, TILE_SIZE * 10)
        ]
        
        # Posiciones iniciales de las momias
        mummy_starts = [
            (TILE_SIZE * 6, TILE_SIZE * 10),
            (TILE_SIZE * 18, TILE_SIZE * 10),
            (TILE_SIZE * 12, TILE_SIZE * 6),
            (TILE_SIZE * 12, TILE_SIZE * 14)
        ]
        
        return Level(width, height, tile_map, player_start, zombie_starts, mummy_starts) 