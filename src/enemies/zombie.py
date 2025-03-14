import pygame
import random
from src.enemies.enemy_base import EnemyBase
from src.utils.constants import ZOMBIE_SPEED, TILE_SIZE
from src.ai.behavior_tree import BehaviorTree, Sequence, Selector, Condition, Action
from src.ai.pathfinding import AStar
from src.utils.image_loader import load_image, create_fallback_surface
import os

class Zombie(EnemyBase):
    def __init__(self, x, y, level):
        super().__init__(x, y, level, ZOMBIE_SPEED, 1, 100)
        self.level = level  # Guardar referencia al nivel
        
        # Cargar sprites
        self.load_sprites()
        
        # Inicializar A* para pathfinding
        self.pathfinder = AStar(level)
        
        # Inicializar árbol de comportamiento
        self.init_behavior_tree(level)
        
        # Camino actual (para A*)
        self.current_path = []
        
        # Estado para el árbol de comportamiento
        self.state = {
            "player_visible": False,
            "player_close": False,
            "random_move_cooldown": 0,
            "last_known_player_pos": None
        }
    
    def load_sprites(self):
        """Carga los sprites del zombie"""
        try:
            self.sprites = {
                "up": [],
                "down": [],
                "left": [],
                "right": []
            }
            
            # Cargar sprites usando la utilidad de carga de imágenes
            for direction in ["up", "down", "left", "right"]:
                for i in range(1, 3):
                    # Definir rutas de archivos
                    png_path = f"assets/images/zombie_{direction}_{i}.png"
                    svg_path = f"assets/images/zombie_{direction}_{i}.svg"
                    
                    # Intentar cargar PNG primero, luego SVG
                    if os.path.exists(png_path):
                        sprite = load_image(png_path, (TILE_SIZE, TILE_SIZE))
                    elif os.path.exists(svg_path):
                        sprite = load_image(svg_path, (TILE_SIZE, TILE_SIZE))
                    else:
                        # Si no existe ninguno, crear un sprite de respaldo
                        print(f"No se encontró ninguna imagen para: zombie_{direction}_{i}")
                        sprite = create_fallback_surface((TILE_SIZE, TILE_SIZE), (144, 238, 144, 255))
                    
                    self.sprites[direction].append(sprite)
        except Exception as e:
            print(f"Error al cargar los sprites del zombie: {e}")
            # Crear sprites de emergencia
            self.create_fallback_sprites()
    
    def create_fallback_sprites(self):
        """Crea sprites de emergencia si no se pueden cargar los normales"""
        self.sprites = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }
        
        # Crear sprites de color sólido para cada dirección
        for direction in self.sprites:
            for _ in range(2):
                sprite = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                sprite.fill((144, 238, 144, 255))  # Color verde claro para zombies
                
                # Añadir detalles básicos según la dirección
                if direction == "up" or direction == "down":
                    # Ojos
                    eye_color = (255, 0, 0)  # Rojo
                    if direction == "down":
                        pygame.draw.circle(sprite, eye_color, (TILE_SIZE//2 - 4, TILE_SIZE//3), 2)
                        pygame.draw.circle(sprite, eye_color, (TILE_SIZE//2 + 4, TILE_SIZE//3), 2)
                
                self.sprites[direction].append(sprite)
    
    def init_behavior_tree(self, level):
        """Inicializa el árbol de comportamiento del zombie"""
        # Condiciones
        is_player_visible = Condition(self.check_player_visible)
        is_player_close = Condition(self.check_player_close)
        has_path = Condition(self.check_has_path)
        
        # Acciones
        chase_player = Action(self.chase_player)
        calculate_path = Action(self.calculate_path_to_player)
        follow_path = Action(self.follow_path)
        move_randomly = Action(self.move_randomly)
        
        # Árbol de comportamiento
        chase_sequence = Sequence([is_player_visible, chase_player])
        pathfind_sequence = Sequence([calculate_path, has_path, follow_path])
        
        main_selector = Selector([
            chase_sequence,
            pathfind_sequence,
            move_randomly
        ])
        
        self.behavior_tree = BehaviorTree(main_selector)
    
    def update(self, player, level):
        """Actualiza el estado del zombie"""
        # Guardar referencia al nivel para usar en otros métodos
        self.level = level
        
        # Actualizar estado
        self.update_state(player, level)
        
        # Ejecutar árbol de comportamiento
        self.behavior_tree.execute(self.state)
        
        # Actualizar animación
        if self.moving:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.animation_frame = (self.animation_frame + 1) % 2
                self.animation_timer = 0
        else:
            self.animation_frame = 0
            self.animation_timer = 0
    
    def update_state(self, player, level):
        """Actualiza el estado del zombie para el árbol de comportamiento"""
        # Comprobar si el jugador es visible (línea de visión)
        self.state["player_visible"] = self.is_player_visible(player, level)
        
        # Comprobar si el jugador está cerca
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        self.state["player_close"] = distance < 150
        
        # Actualizar última posición conocida del jugador
        if self.state["player_visible"]:
            self.state["last_known_player_pos"] = (player.x, player.y)
        
        # Actualizar cooldown de movimiento aleatorio
        if self.state["random_move_cooldown"] > 0:
            self.state["random_move_cooldown"] -= 1
    
    def is_player_visible(self, player, level):
        """Comprueba si hay línea de visión directa al jugador"""
        # Implementación simple de línea de visión
        start_x, start_y = self.x + self.width//2, self.y + self.height//2
        end_x, end_y = player.x + player.width//2, player.y + player.height//2
        
        # Calcular vector dirección
        dx = end_x - start_x
        dy = end_y - start_y
        distance = (dx**2 + dy**2)**0.5
        
        # Si está demasiado lejos, no es visible
        if distance > 200:
            return False
        
        # Comprobar línea de visión
        steps = int(distance / 10)  # Comprobar cada 10 píxeles
        if steps == 0:
            steps = 1
        
        for i in range(1, steps + 1):
            t = i / steps
            check_x = int(start_x + dx * t)
            check_y = int(start_y + dy * t)
            
            # Comprobar si hay colisión con el nivel
            if level.is_collision(check_x, check_y, 1, 1):
                return False
        
        return True
    
    # Métodos para el árbol de comportamiento
    def check_player_visible(self, state):
        """Condición: ¿Es el jugador visible?"""
        return state["player_visible"]
    
    def check_player_close(self, state):
        """Condición: ¿Está el jugador cerca?"""
        return state["player_close"]
    
    def check_has_path(self, state):
        """Condición: ¿Hay un camino disponible?"""
        return len(self.current_path) > 0
    
    def chase_player(self, state):
        """Acción: Perseguir directamente al jugador"""
        if state["last_known_player_pos"] is None:
            return False
        
        target_x, target_y = state["last_known_player_pos"]
        
        # Calcular dirección hacia el jugador
        dx = target_x - self.x
        dy = target_y - self.y
        
        # Normalizar vector de dirección
        length = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / length * self.speed
        dy = dy / length * self.speed
        
        # Actualizar posición
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Actualizar dirección visual
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"
        
        # Comprobar colisiones
        if not self.level.is_collision(new_x, self.y, self.width, self.height):
            self.x = new_x
        
        if not self.level.is_collision(self.x, new_y, self.width, self.height):
            self.y = new_y
        
        self.moving = True
        return True
    
    def calculate_path_to_player(self, state):
        """Acción: Calcular camino hacia el jugador usando A*"""
        if state["last_known_player_pos"] is None:
            return False
        
        target_x, target_y = state["last_known_player_pos"]
        
        # Calcular camino con A*
        self.current_path = self.pathfinder.find_path(
            self.x + self.width//2, 
            self.y + self.height//2,
            target_x + self.width//2, 
            target_y + self.height//2
        )
        
        return True
    
    def follow_path(self, state):
        """Acción: Seguir el camino calculado"""
        if not self.current_path:
            return False
        
        # Obtener siguiente punto del camino
        target_x, target_y = self.current_path[0]
        
        # Calcular dirección hacia el punto
        dx = target_x - (self.x + self.width//2)
        dy = target_y - (self.y + self.height//2)
        
        # Si estamos cerca del punto, pasar al siguiente
        if (dx**2 + dy**2)**0.5 < self.speed:
            self.current_path.pop(0)
            if not self.current_path:
                return True
            target_x, target_y = self.current_path[0]
            dx = target_x - (self.x + self.width//2)
            dy = target_y - (self.y + self.height//2)
        
        # Normalizar vector de dirección
        length = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / length * self.speed
        dy = dy / length * self.speed
        
        # Actualizar posición
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Actualizar dirección visual
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"
        
        # Comprobar colisiones
        if not self.level.is_collision(new_x, self.y, self.width, self.height):
            self.x = new_x
        
        if not self.level.is_collision(self.x, new_y, self.width, self.height):
            self.y = new_y
        
        self.moving = True
        return True
    
    def move_randomly(self, state):
        """Acción: Moverse aleatoriamente"""
        # Si el cooldown está activo, esperar
        if state["random_move_cooldown"] > 0:
            self.moving = False
            return True
        
        # Elegir dirección aleatoria
        directions = ["up", "down", "left", "right"]
        self.direction = random.choice(directions)
        
        # Calcular nueva posición
        dx, dy = 0, 0
        if self.direction == "up":
            dy = -self.speed
        elif self.direction == "down":
            dy = self.speed
        elif self.direction == "left":
            dx = -self.speed
        elif self.direction == "right":
            dx = self.speed
        
        # Actualizar posición
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Comprobar colisiones con el nivel
        if not self.level.is_collision(new_x, self.y, self.width, self.height):
            self.x = new_x
        
        if not self.level.is_collision(self.x, new_y, self.width, self.height):
            self.y = new_y
        
        # Si no se pudo mover, establecer cooldown
        if not self.level.is_collision(new_x, self.y, self.width, self.height):
            state["random_move_cooldown"] = 30  # Esperar 30 frames
            self.moving = False
        else:
            self.moving = True
        
        return True 