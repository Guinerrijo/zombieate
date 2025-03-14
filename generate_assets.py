#!/usr/bin/env python3
# Generador de assets para Zombies Ate My Neighbors
# Autor: [Tu Nombre] - [Tu Matrícula]

import os
import svgwrite
from pathlib import Path

# Crear directorios necesarios
def create_directories():
    directories = [
        "assets",
        "assets/images",
        "assets/sounds",
        "assets/music"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# Generar imágenes de tiles
def generate_tiles():
    # Suelo
    dwg = svgwrite.Drawing('assets/images/floor.svg', size=(32, 32))
    dwg.add(dwg.rect((0, 0), (32, 32), fill='#8B7355'))  # Marrón claro
    # Añadir textura
    for i in range(4):
        for j in range(4):
            dwg.add(dwg.line((i*8, j*8), (i*8+4, j*8+4), stroke='#7A6348', stroke_width=1))
    dwg.save()
    
    # Pared
    dwg = svgwrite.Drawing('assets/images/wall.svg', size=(32, 32))
    dwg.add(dwg.rect((0, 0), (32, 32), fill='#696969'))  # Gris
    # Añadir textura de ladrillos
    for i in range(4):
        dwg.add(dwg.line((0, i*8), (32, i*8), stroke='#505050', stroke_width=1))
    for i in range(4):
        for j in range(2):
            offset = 16 if i % 2 == 0 else 0
            dwg.add(dwg.line((offset + j*32, i*8), (offset + j*32, i*8+8), stroke='#505050', stroke_width=1))
    dwg.save()
    
    # Arbusto
    dwg = svgwrite.Drawing('assets/images/bush.svg', size=(32, 32))
    dwg.add(dwg.rect((0, 0), (32, 32), fill='#8B7355'))  # Fondo marrón
    # Dibujar arbusto
    dwg.add(dwg.circle((16, 16), 12, fill='#228B22'))  # Verde
    dwg.add(dwg.circle((10, 12), 6, fill='#32CD32'))  # Verde claro
    dwg.add(dwg.circle((22, 12), 6, fill='#32CD32'))  # Verde claro
    dwg.add(dwg.circle((16, 22), 6, fill='#32CD32'))  # Verde claro
    dwg.save()
    
    # Agua
    dwg = svgwrite.Drawing('assets/images/water.svg', size=(32, 32))
    dwg.add(dwg.rect((0, 0), (32, 32), fill='#4682B4'))  # Azul
    # Añadir ondas
    for i in range(4):
        dwg.add(dwg.path(d=f'M 0 {8 + i*8} Q 8 {4 + i*8}, 16 {8 + i*8} T 32 {8 + i*8}', 
                         stroke='#87CEFA', stroke_width=1, fill='none'))
    dwg.save()

# Generar sprites del jugador
def generate_player_sprites():
    directions = ['up', 'down', 'left', 'right']
    
    for direction in directions:
        for frame in [1, 2]:
            dwg = svgwrite.Drawing(f'assets/images/player_{direction}_{frame}.svg', size=(32, 32))
            
            # Color base del jugador
            body_color = '#FF6347'  # Rojo-naranja
            head_color = '#FFD700'  # Dorado
            
            # Dibujar cuerpo según dirección
            if direction == 'down':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Ojos
                dwg.add(dwg.circle((14, 7), 1, fill='black'))
                dwg.add(dwg.circle((18, 7), 1, fill='black'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10, 28), (4, 4), fill='blue'))
                dwg.add(dwg.rect((18, 28 + leg_offset), (4, 4), fill='blue'))
                # Brazos
                dwg.add(dwg.rect((6, 14), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=head_color))
                
            elif direction == 'up':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza (vista desde atrás)
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Pelo
                dwg.add(dwg.rect((12, 4), (8, 2), fill='brown'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10, 28 + leg_offset), (4, 4), fill='blue'))
                dwg.add(dwg.rect((18, 28), (4, 4), fill='blue'))
                # Brazos
                dwg.add(dwg.rect((6, 14), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=head_color))
                
            elif direction == 'left':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Ojo (solo se ve uno)
                dwg.add(dwg.circle((14, 7), 1, fill='black'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10 + leg_offset, 28), (4, 4), fill='blue'))
                dwg.add(dwg.rect((18, 28), (4, 4), fill='blue'))
                # Brazos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14 + arm_offset), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=head_color))
                
            elif direction == 'right':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Ojo (solo se ve uno)
                dwg.add(dwg.circle((18, 7), 1, fill='black'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10, 28), (4, 4), fill='blue'))
                dwg.add(dwg.rect((18 + leg_offset, 28), (4, 4), fill='blue'))
                # Brazos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14 + arm_offset), (4, 10), fill=head_color))
            
            dwg.save()

# Generar sprites de zombies
def generate_zombie_sprites():
    directions = ['up', 'down', 'left', 'right']
    
    for direction in directions:
        for frame in [1, 2]:
            dwg = svgwrite.Drawing(f'assets/images/zombie_{direction}_{frame}.svg', size=(32, 32))
            
            # Color base del zombie
            body_color = '#90EE90'  # Verde claro
            head_color = '#90EE90'  # Verde claro
            
            # Dibujar cuerpo según dirección
            if direction == 'down':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Ojos
                dwg.add(dwg.circle((14, 7), 1, fill='red'))
                dwg.add(dwg.circle((18, 7), 1, fill='red'))
                # Boca
                dwg.add(dwg.line((13, 10), (19, 10), stroke='black', stroke_width=1))
                # Piernas
                leg_offset = 3 if frame == 1 else -3
                dwg.add(dwg.rect((10, 28), (4, 4), fill='#556B2F'))
                dwg.add(dwg.rect((18, 28 + leg_offset), (4, 4), fill='#556B2F'))
                # Brazos extendidos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14 + arm_offset), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14 - arm_offset), (4, 10), fill=head_color))
                
            elif direction == 'up':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza (vista desde atrás)
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Pelo despeinado
                for i in range(3):
                    dwg.add(dwg.line((12 + i*4, 4), (12 + i*4, 2), stroke='#556B2F', stroke_width=2))
                # Piernas
                leg_offset = 3 if frame == 1 else -3
                dwg.add(dwg.rect((10, 28 + leg_offset), (4, 4), fill='#556B2F'))
                dwg.add(dwg.rect((18, 28), (4, 4), fill='#556B2F'))
                # Brazos extendidos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14 + arm_offset), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14 - arm_offset), (4, 10), fill=head_color))
                
            elif direction == 'left':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Ojo (solo se ve uno)
                dwg.add(dwg.circle((14, 7), 1, fill='red'))
                # Boca
                dwg.add(dwg.line((13, 10), (16, 10), stroke='black', stroke_width=1))
                # Piernas
                leg_offset = 3 if frame == 1 else -3
                dwg.add(dwg.rect((10 + leg_offset, 28), (4, 4), fill='#556B2F'))
                dwg.add(dwg.rect((18, 28), (4, 4), fill='#556B2F'))
                # Brazos extendidos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14 + arm_offset), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=head_color))
                
            elif direction == 'right':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=head_color))
                # Ojo (solo se ve uno)
                dwg.add(dwg.circle((18, 7), 1, fill='red'))
                # Boca
                dwg.add(dwg.line((16, 10), (19, 10), stroke='black', stroke_width=1))
                # Piernas
                leg_offset = 3 if frame == 1 else -3
                dwg.add(dwg.rect((10, 28), (4, 4), fill='#556B2F'))
                dwg.add(dwg.rect((18 + leg_offset, 28), (4, 4), fill='#556B2F'))
                # Brazos extendidos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14), (4, 10), fill=head_color))
                dwg.add(dwg.rect((22, 14 + arm_offset), (4, 10), fill=head_color))
            
            dwg.save()

# Generar sprites de momias
def generate_mummy_sprites():
    directions = ['up', 'down', 'left', 'right']
    
    for direction in directions:
        for frame in [1, 2]:
            dwg = svgwrite.Drawing(f'assets/images/mummy_{direction}_{frame}.svg', size=(32, 32))
            
            # Color base de la momia
            body_color = '#F5DEB3'  # Beige
            bandage_color = '#FFFFF0'  # Blanco hueso
            
            # Dibujar cuerpo según dirección
            if direction == 'down':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Vendas en el cuerpo
                for i in range(4):
                    dwg.add(dwg.line((10, 14 + i*4), (22, 14 + i*4), stroke=bandage_color, stroke_width=2))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=body_color))
                # Vendas en la cabeza
                dwg.add(dwg.line((10, 8), (22, 8), stroke=bandage_color, stroke_width=2))
                dwg.add(dwg.line((16, 2), (16, 14), stroke=bandage_color, stroke_width=2))
                # Ojos
                dwg.add(dwg.circle((14, 7), 1, fill='red'))
                dwg.add(dwg.circle((18, 7), 1, fill='red'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10, 28), (4, 4), fill=body_color))
                dwg.add(dwg.rect((18, 28 + leg_offset), (4, 4), fill=body_color))
                # Vendas en las piernas
                dwg.add(dwg.line((10, 30), (14, 30), stroke=bandage_color, stroke_width=1))
                dwg.add(dwg.line((18, 30 + leg_offset), (22, 30 + leg_offset), stroke=bandage_color, stroke_width=1))
                # Brazos extendidos
                dwg.add(dwg.rect((6, 14), (4, 10), fill=body_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=body_color))
                # Vendas en los brazos
                for i in range(3):
                    dwg.add(dwg.line((6, 16 + i*4), (10, 16 + i*4), stroke=bandage_color, stroke_width=1))
                    dwg.add(dwg.line((22, 16 + i*4), (26, 16 + i*4), stroke=bandage_color, stroke_width=1))
                
            elif direction == 'up':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Vendas en el cuerpo
                for i in range(4):
                    dwg.add(dwg.line((10, 14 + i*4), (22, 14 + i*4), stroke=bandage_color, stroke_width=2))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=body_color))
                # Vendas en la cabeza
                dwg.add(dwg.line((10, 8), (22, 8), stroke=bandage_color, stroke_width=2))
                dwg.add(dwg.line((16, 2), (16, 14), stroke=bandage_color, stroke_width=2))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10, 28 + leg_offset), (4, 4), fill=body_color))
                dwg.add(dwg.rect((18, 28), (4, 4), fill=body_color))
                # Vendas en las piernas
                dwg.add(dwg.line((10, 30 + leg_offset), (14, 30 + leg_offset), stroke=bandage_color, stroke_width=1))
                dwg.add(dwg.line((18, 30), (22, 30), stroke=bandage_color, stroke_width=1))
                # Brazos extendidos
                dwg.add(dwg.rect((6, 14), (4, 10), fill=body_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=body_color))
                # Vendas en los brazos
                for i in range(3):
                    dwg.add(dwg.line((6, 16 + i*4), (10, 16 + i*4), stroke=bandage_color, stroke_width=1))
                    dwg.add(dwg.line((22, 16 + i*4), (26, 16 + i*4), stroke=bandage_color, stroke_width=1))
                
            elif direction == 'left':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Vendas en el cuerpo
                for i in range(4):
                    dwg.add(dwg.line((10, 14 + i*4), (22, 14 + i*4), stroke=bandage_color, stroke_width=2))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=body_color))
                # Vendas en la cabeza
                dwg.add(dwg.line((10, 8), (22, 8), stroke=bandage_color, stroke_width=2))
                dwg.add(dwg.line((16, 2), (16, 14), stroke=bandage_color, stroke_width=2))
                # Ojo (solo se ve uno)
                dwg.add(dwg.circle((14, 7), 1, fill='red'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10 + leg_offset, 28), (4, 4), fill=body_color))
                dwg.add(dwg.rect((18, 28), (4, 4), fill=body_color))
                # Vendas en las piernas
                dwg.add(dwg.line((10 + leg_offset, 30), (14 + leg_offset, 30), stroke=bandage_color, stroke_width=1))
                dwg.add(dwg.line((18, 30), (22, 30), stroke=bandage_color, stroke_width=1))
                # Brazos extendidos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14 + arm_offset), (4, 10), fill=body_color))
                dwg.add(dwg.rect((22, 14), (4, 10), fill=body_color))
                # Vendas en los brazos
                for i in range(3):
                    dwg.add(dwg.line((6, 16 + arm_offset + i*4), (10, 16 + arm_offset + i*4), stroke=bandage_color, stroke_width=1))
                    dwg.add(dwg.line((22, 16 + i*4), (26, 16 + i*4), stroke=bandage_color, stroke_width=1))
                
            elif direction == 'right':
                # Cuerpo
                dwg.add(dwg.rect((10, 12), (12, 16), fill=body_color))
                # Vendas en el cuerpo
                for i in range(4):
                    dwg.add(dwg.line((10, 14 + i*4), (22, 14 + i*4), stroke=bandage_color, stroke_width=2))
                # Cabeza
                dwg.add(dwg.circle((16, 8), 6, fill=body_color))
                # Vendas en la cabeza
                dwg.add(dwg.line((10, 8), (22, 8), stroke=bandage_color, stroke_width=2))
                dwg.add(dwg.line((16, 2), (16, 14), stroke=bandage_color, stroke_width=2))
                # Ojo (solo se ve uno)
                dwg.add(dwg.circle((18, 7), 1, fill='red'))
                # Piernas
                leg_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((10, 28), (4, 4), fill=body_color))
                dwg.add(dwg.rect((18 + leg_offset, 28), (4, 4), fill=body_color))
                # Vendas en las piernas
                dwg.add(dwg.line((10, 30), (14, 30), stroke=bandage_color, stroke_width=1))
                dwg.add(dwg.line((18 + leg_offset, 30), (22 + leg_offset, 30), stroke=bandage_color, stroke_width=1))
                # Brazos extendidos
                arm_offset = 2 if frame == 1 else -2
                dwg.add(dwg.rect((6, 14), (4, 10), fill=body_color))
                dwg.add(dwg.rect((22, 14 + arm_offset), (4, 10), fill=body_color))
                # Vendas en los brazos
                for i in range(3):
                    dwg.add(dwg.line((6, 16 + i*4), (10, 16 + i*4), stroke=bandage_color, stroke_width=1))
                    dwg.add(dwg.line((22, 16 + arm_offset + i*4), (26, 16 + arm_offset + i*4), stroke=bandage_color, stroke_width=1))
            
            dwg.save()

# Generar proyectil de agua
def generate_water_projectile():
    dwg = svgwrite.Drawing('assets/images/water_projectile.svg', size=(16, 16))
    # Gota de agua
    dwg.add(dwg.circle((8, 8), 6, fill='#1E90FF'))  # Azul
    # Brillo
    dwg.add(dwg.circle((6, 6), 2, fill='#87CEFA'))  # Azul claro
    dwg.save()

# Generar icono de salud
def generate_health_icon():
    dwg = svgwrite.Drawing('assets/images/health_icon.svg', size=(24, 24))
    # Corazón
    dwg.add(dwg.path(d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z', 
                     fill='red'))
    dwg.save()

# Generar fondo del menú
def generate_menu_background():
    dwg = svgwrite.Drawing('assets/images/menu_background.svg', size=(800, 600))
    # Fondo oscuro
    dwg.add(dwg.rect((0, 0), (800, 600), fill='#000033'))
    
    # Cementerio en el fondo
    for i in range(10):
        x = 50 + i * 80
        y = 400
        # Lápida
        dwg.add(dwg.rect((x, y), (30, 50), fill='#808080'))
        dwg.add(dwg.rect((x-5, y-10), (40, 10), fill='#A9A9A9'))
        
    # Luna
    dwg.add(dwg.circle((650, 100), 40, fill='#FFFACD'))
    dwg.add(dwg.circle((630, 90), 10, fill='#000033'))
    
    # Nubes oscuras
    for i in range(5):
        x = 100 + i * 150
        y = 150 + (i % 3) * 30
        for j in range(3):
            dwg.add(dwg.circle((x + j*30, y), 25, fill='#483D8B', opacity=0.7))
    
    # Casa embrujada
    dwg.add(dwg.rect((300, 250), (200, 150), fill='#8B4513'))
    dwg.add(dwg.polygon([(300, 250), (500, 250), (400, 180)], fill='#A52A2A'))
    # Ventanas
    dwg.add(dwg.rect((330, 280), (40, 40), fill='#FFD700'))
    dwg.add(dwg.rect((430, 280), (40, 40), fill='#FFD700'))
    dwg.add(dwg.line((350, 280), (350, 320), stroke='black', stroke_width=2))
    dwg.add(dwg.line((330, 300), (370, 300), stroke='black', stroke_width=2))
    dwg.add(dwg.line((450, 280), (450, 320), stroke='black', stroke_width=2))
    dwg.add(dwg.line((430, 300), (470, 300), stroke='black', stroke_width=2))
    # Puerta
    dwg.add(dwg.rect((380, 330), (40, 70), fill='#8B0000'))
    
    # Zombies en silueta
    for i in range(3):
        x = 100 + i * 250
        y = 500
        # Cuerpo
        dwg.add(dwg.rect((x, y), (20, 30), fill='black', opacity=0.8))
        # Cabeza
        dwg.add(dwg.circle((x+10, y-10), 10, fill='black', opacity=0.8))
        # Brazos extendidos
        dwg.add(dwg.rect((x-10, y+5), (10, 5), fill='black', opacity=0.8))
        dwg.add(dwg.rect((x+20, y+5), (10, 5), fill='black', opacity=0.8))
    
    dwg.save()

# Generar sonidos simples
def generate_sounds():
    # Crear archivos de sonido vacíos (0.5 segundos de silencio)
    # En un proyecto real, deberías usar sonidos reales
    sample_rate = 44100
    duration = 0.5  # segundos
    
    # Generar un buffer de audio con silencio
    buffer = bytearray(int(sample_rate * duration))
    
    # Guardar los archivos de sonido
    sound_files = [
        "assets/sounds/shoot.wav",
        "assets/sounds/hit.wav",
        "assets/sounds/pickup.wav",
        "assets/sounds/death.wav",
        "assets/sounds/victory.wav",
        "assets/sounds/select.wav"
    ]
    
    # Crear archivos de sonido vacíos
    for sound_file in sound_files:
        with open(sound_file, 'wb') as f:
            f.write(buffer)
    
    # Crear archivos de música vacíos
    music_files = [
        "assets/music/menu.mp3",
        "assets/music/level1.mp3"
    ]
    
    for music_file in music_files:
        with open(music_file, 'wb') as f:
            f.write(buffer)

# Función principal 