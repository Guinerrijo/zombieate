import pygame
from src.utils.constants import PLAYER_SPEED, PLAYER_HEALTH, TILE_SIZE
import os

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.active = True
        
        # Cargar sprite
        sprite = None
        png_path = "assets/images/water_projectile.png"
        svg_path = "assets/images/water_projectile.svg"
        
        try:
            # Intentar cargar PNG primero
            if os.path.exists(png_path):
                sprite = pygame.image.load(png_path)
                sprite = pygame.transform.scale(sprite, (16, 16))
            # Si no hay PNG, intentar cargar SVG
            elif os.path.exists(svg_path):
                try:
                    # Método 1: Cargar directamente con pygame 2.0+
                    sprite = pygame.image.load(svg_path)
                    sprite = pygame.transform.scale(sprite, (16, 16))
                except pygame.error:
                    # Método 2: Intentar usar cairosvg si está disponible
                    try:
                        import cairosvg
                        import io
                        png_bytes = cairosvg.svg2png(url=svg_path)
                        byte_io = io.BytesIO(png_bytes)
                        sprite = pygame.image.load(byte_io)
                        sprite = pygame.transform.scale(sprite, (16, 16))
                    except (ImportError, ModuleNotFoundError):
                        print(f"No se pudo cargar cairosvg para convertir {svg_path}")
                        sprite = None
        except pygame.error as e:
            print(f"Error al cargar sprite de proyectil: {e}")
            sprite = None
        
        # Si no se pudo cargar, crear un sprite por defecto
        if sprite is None:
            print("No se pudo cargar el sprite del proyectil")
            sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            sprite.fill((30, 144, 255, 192))  # Color azul semitransparente para el agua
            # Añadir un brillo
            pygame.draw.circle(sprite, (135, 206, 250), (6, 6), 3)
        
        self.sprite = sprite
    
    def update(self):
        """Actualiza la posición del proyectil"""
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
    
    def get_collision_rect(self):
        """Devuelve el rectángulo de colisión del proyectil"""
        return pygame.Rect(self.x, self.y, 16, 16)
    
    def render(self, screen):
        """Renderiza el proyectil en pantalla"""
        screen.blit(self.sprite, (self.x, self.y))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.direction = "down"  # Dirección inicial
        self.moving = False
        self.shooting = False
        self.projectiles = []
        
        # Cargar sprites
        self.load_sprites()
        
        # Cargar sonidos
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.mp3")
        
        # Animación
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
    
    def load_sprites(self):
        """Carga los sprites del jugador"""
        try:
            self.sprites = {
                "up": [],
                "down": [],
                "left": [],
                "right": []
            }
            
            # Intentar cargar primero PNG, luego SVG como respaldo
            for direction in ["up", "down", "left", "right"]:
                for i in range(1, 3):
                    sprite = None
                    # Intentar cargar PNG primero
                    png_path = f"assets/images/player_{direction}_{i}.png"
                    svg_path = f"assets/images/player_{direction}_{i}.svg"
                    
                    try:
                        # Intentar cargar PNG primero
                        if os.path.exists(png_path):
                            sprite = pygame.image.load(png_path)
                        # Si no hay PNG, intentar cargar SVG
                        elif os.path.exists(svg_path):
                            try:
                                # Método 1: Cargar directamente con pygame 2.0+
                                sprite = pygame.image.load(svg_path)
                            except pygame.error:
                                # Método 2: Intentar usar cairosvg si está disponible
                                try:
                                    import cairosvg
                                    import io
                                    png_bytes = cairosvg.svg2png(url=svg_path)
                                    byte_io = io.BytesIO(png_bytes)
                                    sprite = pygame.image.load(byte_io)
                                except (ImportError, ModuleNotFoundError):
                                    print(f"No se pudo cargar cairosvg para convertir {svg_path}")
                                    sprite = None
                    except pygame.error as e:
                        print(f"Error al cargar sprite: {e}")
                        sprite = None
                    
                    # Si no se pudo cargar, crear un sprite de color sólido
                    if sprite is None:
                        print(f"No se pudo cargar el sprite: player_{direction}_{i}")
                        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        sprite.fill((255, 99, 71, 255))  # Color rojo-naranja para el jugador
                    
                    self.sprites[direction].append(sprite)
            
            # Escalar sprites
            for direction in self.sprites:
                for i in range(len(self.sprites[direction])):
                    self.sprites[direction][i] = pygame.transform.scale(
                        self.sprites[direction][i], (self.width, self.height)
                    )
        except Exception as e:
            print(f"Error al cargar los sprites del jugador: {e}")
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
                sprite.fill((255, 99, 71, 255))  # Color rojo-naranja para el jugador
                
                # Añadir detalles básicos según la dirección
                if direction == "up" or direction == "down":
                    # Cabeza
                    pygame.draw.circle(sprite, (255, 215, 0), (TILE_SIZE//2, TILE_SIZE//3), TILE_SIZE//6)
                    
                    # Ojos
                    if direction == "down":
                        pygame.draw.circle(sprite, (0, 0, 0), (TILE_SIZE//2 - 2, TILE_SIZE//3 - 1), 1)
                        pygame.draw.circle(sprite, (0, 0, 0), (TILE_SIZE//2 + 2, TILE_SIZE//3 - 1), 1)
                
                self.sprites[direction].append(sprite)
                
    def handle_event(self, event):
        """Maneja los eventos del jugador"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shoot()
    
    def update(self, level):
        """Actualiza el estado del jugador"""
        # Movimiento
        keys = pygame.key.get_pressed()
        
        dx, dy = 0, 0
        self.moving = False
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"
            self.moving = True
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"
            self.moving = True
        
        # Comprobar colisiones con el nivel
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Comprobar colisiones en X
        if not level.is_collision(new_x, self.y, self.width, self.height):
            self.x = new_x
        
        # Comprobar colisiones en Y
        if not level.is_collision(self.x, new_y, self.width, self.height):
            self.y = new_y
        
        # Actualizar animación
        if self.moving:
            self.animation_timer += 1
            if self.animation_timer >= 10:  # Cambiar frame cada 10 actualizaciones
                self.animation_frame = (self.animation_frame + 1) % 2
                self.animation_timer = 0
        else:
            self.animation_frame = 0
            self.animation_timer = 0
        
        # Actualizar proyectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Eliminar proyectiles que salen de la pantalla
            if (projectile.x < 0 or projectile.x > level.width * TILE_SIZE or
                projectile.y < 0 or projectile.y > level.height * TILE_SIZE):
                self.projectiles.remove(projectile)
            
            # Comprobar colisiones con el nivel
            if level.is_collision(projectile.x, projectile.y, 16, 16):
                self.projectiles.remove(projectile)
    
    def shoot(self):
        """Dispara un proyectil en la dirección actual"""
        # Posición inicial del proyectil (centro del jugador)
        proj_x = self.x + self.width // 2 - 8
        proj_y = self.y + self.height // 2 - 8
        
        # Ajustar posición según dirección
        if self.direction == "up":
            proj_y -= self.height // 2
        elif self.direction == "down":
            proj_y += self.height // 2
        elif self.direction == "left":
            proj_x -= self.width // 2
        elif self.direction == "right":
            proj_x += self.width // 2
        
        # Crear y añadir proyectil
        self.projectiles.append(Projectile(proj_x, proj_y, self.direction))
        
        # Reproducir sonido de disparo
        try:
            self.shoot_sound.play()
        except:
            print("No se pudo reproducir el sonido de disparo")
    
    def take_damage(self):
        """Reduce la salud del jugador"""
        self.health -= 1
    
    def get_collision_rect(self):
        """Devuelve el rectángulo de colisión del jugador"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen):
        """Renderiza al jugador y sus proyectiles en pantalla"""
        # Dibujar jugador
        current_sprite = self.sprites[self.direction][self.animation_frame]
        screen.blit(current_sprite, (self.x, self.y))
        
        # Dibujar proyectiles
        for projectile in self.projectiles:
            projectile.render(screen) 