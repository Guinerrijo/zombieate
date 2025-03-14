import pygame
import random
from src.utils.constants import TILE_SIZE
from src.utils.image_loader import load_image, create_fallback_surface
import os

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.width = 20  # Ancho en tiles
        self.height = 15  # Alto en tiles
        
        # Cargar mapa
        self.load_map()
        
        # Cargar sprites de tiles
        self.load_tiles()
    
    def load_map(self):
        """Carga o genera el mapa del nivel"""
        # Ejemplo simple: generar un mapa aleatorio con paredes en los bordes
        self.map = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Paredes en los bordes
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    row.append(1)  # 1 = pared
                # Algunas paredes aleatorias en el interior
                elif random.random() < 0.2:
                    row.append(1)  # 1 = pared
                else:
                    row.append(0)  # 0 = suelo
            self.map.append(row)
        
        # Asegurar que hay un camino desde el inicio hasta algún punto del mapa
        self.ensure_playable()
    
    def ensure_playable(self):
        """Asegura que el mapa es jugable (hay camino desde el inicio)"""
        # Simplemente limpiar un área alrededor del punto de inicio
        start_x, start_y = 2, 2
        for y in range(start_y - 1, start_y + 2):
            for x in range(start_x - 1, start_x + 2):
                if 0 <= y < self.height and 0 <= x < self.width:
                    self.map[y][x] = 0  # Asegurar que es suelo
    
    def load_tiles(self):
        """Carga los sprites de los tiles"""
        try:
            # Definir rutas de archivos
            floor_png = "assets/images/floor.png"
            floor_svg = "assets/images/floor.svg"
            wall_png = "assets/images/wall.png"
            wall_svg = "assets/images/wall.svg"
            
            # Cargar tile de suelo
            if os.path.exists(floor_png):
                self.floor_tile = load_image(floor_png, (TILE_SIZE, TILE_SIZE))
            elif os.path.exists(floor_svg):
                self.floor_tile = load_image(floor_svg, (TILE_SIZE, TILE_SIZE))
            else:
                print("No se encontró imagen para el suelo, usando respaldo")
                self.floor_tile = self.create_default_floor_tile()
            
            # Cargar tile de pared
            if os.path.exists(wall_png):
                self.wall_tile = load_image(wall_png, (TILE_SIZE, TILE_SIZE))
            elif os.path.exists(wall_svg):
                self.wall_tile = load_image(wall_svg, (TILE_SIZE, TILE_SIZE))
            else:
                print("No se encontró imagen para la pared, usando respaldo")
                self.wall_tile = self.create_default_wall_tile()
                
        except Exception as e:
            print(f"Error al cargar los tiles: {e}")
            self.create_default_tiles()
    
    def create_default_floor_tile(self):
        """Crea un tile de suelo por defecto"""
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.fill((139, 115, 85))  # Marrón claro
        
        # Añadir textura al suelo
        for i in range(4):
            for j in range(4):
                pygame.draw.line(
                    tile, 
                    (122, 99, 72), 
                    (i*8, j*8), 
                    (i*8+4, j*8+4), 
                    1
                )
        return tile
    
    def create_default_wall_tile(self):
        """Crea un tile de pared por defecto"""
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.fill((105, 105, 105))  # Gris
        
        # Añadir textura de ladrillos
        for i in range(4):
            pygame.draw.line(
                tile, 
                (80, 80, 80), 
                (0, i*8), 
                (TILE_SIZE, i*8), 
                1
            )
        
        for i in range(4):
            for j in range(2):
                offset = 16 if i % 2 == 0 else 0
                pygame.draw.line(
                    tile, 
                    (80, 80, 80), 
                    (i*8 + offset, j*16), 
                    (i*8 + offset, j*16 + 8), 
                    1
                )
        return tile
    
    def create_default_tiles(self):
        """Crea tiles por defecto cuando no se pueden cargar las imágenes"""
        self.floor_tile = self.create_default_floor_tile()
        self.wall_tile = self.create_default_wall_tile()
    
    def get_player_start(self):
        """Devuelve la posición inicial del jugador"""
        return (2 * TILE_SIZE, 2 * TILE_SIZE)
    
    def is_collision(self, x, y, width, height):
        """Comprueba si hay colisión en la posición dada"""
        # Convertir coordenadas de píxeles a coordenadas de tiles
        tile_x1 = max(0, int(x // TILE_SIZE))
        tile_y1 = max(0, int(y // TILE_SIZE))
        tile_x2 = min(self.width - 1, int((x + width - 1) // TILE_SIZE))
        tile_y2 = min(self.height - 1, int((y + height - 1) // TILE_SIZE))
        
        # Comprobar cada tile en el área
        for ty in range(tile_y1, tile_y2 + 1):
            for tx in range(tile_x1, tile_x2 + 1):
                if ty < len(self.map) and tx < len(self.map[ty]):
                    tile_type = self.map[ty][tx]
                    if tile_type == 1:  # 1 representa una pared
                        return True
        
        return False
    
    def render(self, screen):
        """Renderiza el nivel en pantalla"""
        for y in range(self.height):
            for x in range(self.width):
                # Dibujar suelo en todas partes
                screen.blit(self.floor_tile, (x * TILE_SIZE, y * TILE_SIZE))
                
                # Dibujar paredes donde corresponda
                if self.map[y][x] == 1:
                    screen.blit(self.wall_tile, (x * TILE_SIZE, y * TILE_SIZE))
    
    def is_tile_blocked(self, tile_x, tile_y):
        """Comprueba si un tile está bloqueado (es una pared)"""
        # Verificar que las coordenadas están dentro de los límites
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.map[tile_y][tile_x] == 1  # 1 representa una pared
        # Si está fuera de los límites, considerarlo como bloqueado
        return True 