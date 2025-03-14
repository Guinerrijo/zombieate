import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, YELLOW
from src.utils.image_loader import load_image, create_fallback_surface
import os

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        
        # Cargar fondo y música del menú
        bg_png = "assets/images/menu_background.png"
        bg_svg = "assets/images/menu_background.svg"
        
        if os.path.exists(bg_png):
            self.background = load_image(bg_png, (SCREEN_WIDTH, SCREEN_HEIGHT))
        elif os.path.exists(bg_svg):
            self.background = load_image(bg_svg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            print("No se encontró imagen para el fondo del menú, usando respaldo")
            self.background = self.create_default_background()
        
        # Cargar sonidos
        try:
            self.select_sound = pygame.mixer.Sound("assets/sounds/select.mp3")
        except pygame.error:
            print("No se pudo cargar el sonido de selección")
            self.select_sound = pygame.mixer.Sound(buffer=bytes([0] * 44100))  # Sonido vacío
        
        # Opciones del menú
        self.options = ["Iniciar Juego", "Salir"]
        self.selected_option = 0
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 48)
        
        # Iniciar música del menú
        try:
            pygame.mixer.music.load("assets/music/menu.mp3")
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("No se pudo cargar la música del menú")
    
    def create_default_background(self):
        """Crea un fondo por defecto para el menú"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((50, 50, 100))  # Azul oscuro
        
        # Añadir un poco de textura
        for i in range(0, SCREEN_WIDTH, 20):
            for j in range(0, SCREEN_HEIGHT, 20):
                if (i + j) % 40 == 0:
                    pygame.draw.rect(bg, (60, 60, 120), (i, j, 10, 10))
        
        return bg
    
    def handle_event(self, event):
        """Maneja los eventos del menú"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.select_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.select_sound.play()
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Iniciar Juego
                    pygame.mixer.music.stop()
                    self.game.reset_game()
                    return "game"
                elif self.selected_option == 1:  # Salir
                    pygame.quit()
                    exit()
        
        return None
    
    def update(self):
        """Actualiza el estado del menú"""
        pass  # No hay nada que actualizar en el menú por ahora
    
    def render(self):
        """Renderiza el menú en pantalla"""
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))
        
        # Dibujar título
        title_text = self.title_font.render("Zombies Ate My Neighbors", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        # Dibujar opciones
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 60))
            self.screen.blit(option_text, option_rect) 