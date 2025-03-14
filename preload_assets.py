#!/usr/bin/env python3
"""
Script para precargar y convertir todos los assets antes de iniciar el juego
"""
import os
import pygame
import time
from convert_svg_to_png import convert_all_svg_to_png

def main():
    """Función principal para precargar assets"""
    print("Iniciando precarga de assets...")
    start_time = time.time()
    
    # Inicializar pygame (necesario para operaciones de imagen)
    pygame.init()
    
    # Convertir SVG a PNG
    print("\n=== Convirtiendo SVG a PNG ===")
    convert_all_svg_to_png()
    
    # Verificar que todos los archivos necesarios existen
    print("\n=== Verificando archivos de imagen ===")
    check_image_files()
    
    # Mostrar tiempo total
    elapsed_time = time.time() - start_time
    print(f"\nPrecarga completada en {elapsed_time:.2f} segundos")
    print("Ahora puedes iniciar el juego con 'python main.py'")

def check_image_files():
    """Verifica que todos los archivos de imagen necesarios existen"""
    # Lista de prefijos de archivos que deberían existir
    prefixes = [
        "player_up", "player_down", "player_left", "player_right",
        "zombie_up", "zombie_down", "zombie_left", "zombie_right",
        "mummy_up", "mummy_down", "mummy_left", "mummy_right",
        "water_projectile", "health_icon", "menu_background",
        "floor", "wall", "bush", "water"
    ]
    
    missing_files = []
    
    for prefix in prefixes:
        # Verificar si existe al menos un archivo con este prefijo (PNG o SVG)
        found = False
        for ext in [".png", ".svg"]:
            pattern = f"assets/images/{prefix}*{ext}"
            import glob
            if glob.glob(pattern):
                found = True
                break
        
        if not found:
            missing_files.append(prefix)
    
    if missing_files:
        print(f"ADVERTENCIA: No se encontraron archivos para estos prefijos: {', '.join(missing_files)}")
    else:
        print("Todos los archivos de imagen necesarios están presentes")

if __name__ == "__main__":
    main() 