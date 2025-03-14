import pygame
import sys
from src.game import Game
from src.ui.menu import Menu
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

def main():
    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configurar la ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    # Crear instancias del juego y el menú
    game = Game(screen)
    menu = Menu(screen, game)
    
    # Estado actual (menú o juego)
    current_state = "menu"
    
    # Bucle principal
    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pasar eventos al estado actual
            if current_state == "menu":
                new_state = menu.handle_event(event)
                if new_state:
                    current_state = new_state
            elif current_state == "game":
                new_state = game.handle_event(event)
                if new_state:
                    current_state = new_state
        
        # Actualizar y renderizar el estado actual
        if current_state == "menu":
            menu.update()
            menu.render()
        elif current_state == "game":
            game.update()
            game.render()
        
        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(FPS)
    
    # Limpiar y salir
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 