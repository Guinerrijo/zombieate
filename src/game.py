import pygame
import random
from src.player import Player
from src.level import Level
from src.enemies.zombie import Zombie
from src.enemies.mummy import Mummy
from src.levels.level_loader import LevelLoader
from src.ui.hud import HUD
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.is_running = False
        self.level_number = 1
        self.score = 0
        self.game_over = False
        self.victory = False
        
        # Cargar sonidos
        self.load_sounds()
        
        # Inicializar componentes del juego
        self.reset_game()
    
    def reset_game(self):
        """Reinicia el juego al estado inicial"""
        # Cargar nivel
        self.current_level = Level(self.level_number)
        
        # Crear jugador en posición inicial
        player_start = self.current_level.get_player_start()
        self.player = Player(player_start[0], player_start[1])
        
        # Definir número de enemigos según el nivel
        num_zombies = 2 + self.level_number  # Aumenta con el nivel
        num_mummies = self.level_number // 2  # Aparecen en niveles más avanzados
        
        # Crear enemigos
        self.enemies = []
        
        # Generar posiciones válidas para los enemigos
        valid_enemy_positions = self.generate_valid_enemy_positions(num_zombies + num_mummies)
        
        # Crear zombies
        for i in range(num_zombies):
            if i < len(valid_enemy_positions):
                pos = valid_enemy_positions[i]
                self.enemies.append(Zombie(pos[0], pos[1], self.current_level))
        
        # Crear momias
        for i in range(num_mummies):
            if i + num_zombies < len(valid_enemy_positions):
                pos = valid_enemy_positions[i + num_zombies]
                self.enemies.append(Mummy(pos[0], pos[1], self.current_level))
        
        # Inicializar otros elementos del juego
        self.items = []
        self.generate_items()
        
        # Reiniciar estado del juego
        self.game_over = False
        self.victory = False
        self.score = 0
        self.time_remaining = 120  # 2 minutos por nivel
        
        # Crear HUD
        self.hud = HUD(self)
        
        # Iniciar música
        try:
            pygame.mixer.music.load("assets/music/level1.mp3")
            pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
        except pygame.error:
            print("No se pudo cargar la música del nivel")
    
    def load_sounds(self):
        """Carga los efectos de sonido del juego"""
        self.sounds = {}
        
        # Lista de sonidos a cargar
        sound_files = {
            "shoot": "assets/sounds/shoot.mp3",
            "hit": "assets/sounds/hit.wav",
            "pickup": "assets/sounds/pickup.mp3",
            "death": "assets/sounds/death.mp3",
            "victory": "assets/sounds/victory.mp3"
        }
        
        # Intentar cargar cada sonido
        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"No se pudo cargar el sonido: {path}")
                # Crear un sonido vacío como respaldo
                self.sounds[name] = pygame.mixer.Sound(buffer=bytes([0] * 44100))
    
    def handle_event(self, event):
        """Maneja los eventos del juego"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_r and (self.game_over or self.victory):
                self.reset_game()
        
        # Pasar eventos al jugador
        if not self.game_over and not self.victory:
            self.player.handle_event(event)
        
        return None
    
    def update(self):
        """Actualiza el estado del juego"""
        if self.game_over or self.victory:
            return
        
        # Actualizar jugador
        self.player.update(self.current_level)
        
        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.update(self.player, self.current_level)
        
        # Comprobar colisiones
        self.check_collisions()
        
        # Comprobar condiciones de victoria/derrota
        self.check_game_state()
    
    def check_collisions(self):
        """Comprueba colisiones entre entidades"""
        # Colisiones jugador-enemigo
        player_rect = self.player.get_collision_rect()
        for enemy in self.enemies:
            enemy_rect = enemy.get_collision_rect()
            if player_rect.colliderect(enemy_rect):
                self.player.take_damage()
                self.sounds["hit"].play()
                
                # Comprobar si el jugador ha muerto
                if self.player.health <= 0:
                    self.game_over = True
                    self.sounds["death"].play()
                    pygame.mixer.music.stop()
        
        # Colisiones proyectil-enemigo
        for projectile in self.player.projectiles:
            projectile_rect = projectile.get_collision_rect()
            for enemy in self.enemies[:]:  # Usar copia para poder eliminar durante la iteración
                enemy_rect = enemy.get_collision_rect()
                if projectile_rect.colliderect(enemy_rect):
                    enemy.take_damage()
                    self.player.projectiles.remove(projectile)
                    
                    # Si el enemigo muere
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += enemy.score_value
                    break
    
    def check_game_state(self):
        """Comprueba si se han cumplido las condiciones de victoria o derrota"""
        # Victoria si no quedan enemigos
        if len(self.enemies) == 0:
            self.victory = True
            self.sounds["victory"].play()
            pygame.mixer.music.stop()
    
    def render(self):
        """Renderiza el juego en pantalla"""
        # Dibujar fondo
        self.screen.fill((0, 0, 0))
        
        # Dibujar nivel
        self.current_level.render(self.screen)
        
        # Dibujar jugador
        self.player.render(self.screen)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        # Dibujar HUD
        self.hud.render(self.screen)
        
        # Mostrar mensaje de fin de juego si es necesario
        if self.game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 36)
            text = font.render("Presiona R para reiniciar", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(text, text_rect)
        
        elif self.victory:
            font = pygame.font.Font(None, 72)
            text = font.render("¡VICTORIA!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 36)
            text = font.render("Presiona R para reiniciar", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(text, text_rect)
    
    def generate_valid_enemy_positions(self, num_positions):
        """Genera posiciones válidas para los enemigos (sin colisiones con paredes)"""
        valid_positions = []
        attempts = 0
        max_attempts = 1000  # Límite para evitar bucles infinitos
        
        while len(valid_positions) < num_positions and attempts < max_attempts:
            # Generar posición aleatoria
            x = random.randint(2, self.current_level.width - 3) * TILE_SIZE
            y = random.randint(2, self.current_level.height - 3) * TILE_SIZE
            
            # Verificar que no colisiona con paredes
            if not self.current_level.is_collision(x, y, TILE_SIZE, TILE_SIZE):
                # Verificar que está a una distancia mínima del jugador
                player_distance = ((x - self.player.x)**2 + (y - self.player.y)**2)**0.5
                min_distance = 5 * TILE_SIZE  # Al menos 5 tiles de distancia
                
                if player_distance >= min_distance:
                    # Verificar que no está demasiado cerca de otros enemigos
                    too_close = False
                    for pos in valid_positions:
                        enemy_distance = ((x - pos[0])**2 + (y - pos[1])**2)**0.5
                        if enemy_distance < 3 * TILE_SIZE:  # Al menos 3 tiles de separación
                            too_close = True
                            break
                    
                    if not too_close:
                        valid_positions.append((x, y))
            
            attempts += 1
        
        # Si no se encontraron suficientes posiciones, rellenar con posiciones por defecto
        if len(valid_positions) < num_positions:
            print(f"Advertencia: Solo se encontraron {len(valid_positions)} posiciones válidas para enemigos")
            
            # Añadir posiciones por defecto en los bordes del mapa
            default_positions = [
                (2 * TILE_SIZE, 2 * TILE_SIZE),
                ((self.current_level.width - 3) * TILE_SIZE, 2 * TILE_SIZE),
                (2 * TILE_SIZE, (self.current_level.height - 3) * TILE_SIZE),
                ((self.current_level.width - 3) * TILE_SIZE, (self.current_level.height - 3) * TILE_SIZE)
            ]
            
            for pos in default_positions:
                if len(valid_positions) < num_positions and pos not in valid_positions:
                    valid_positions.append(pos)
        
        return valid_positions
        
    def generate_items(self):
        """Genera ítems en el nivel"""
        # Por ahora, no generamos ítems
        # Esta función se puede implementar más adelante para añadir
        # power-ups, llaves, etc.
        pass 