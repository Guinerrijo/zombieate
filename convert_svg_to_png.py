#!/usr/bin/env python3
"""
Script para convertir archivos SVG a PNG
"""
import os
import glob
import pygame
from src.utils.image_loader import convert_svg_to_png

def convert_all_svg_to_png():
    """Convierte todos los archivos SVG en la carpeta assets/images a PNG"""
    # Asegurarse de que el directorio existe
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images", exist_ok=True)
    
    # Buscar todos los archivos SVG
    svg_files = glob.glob("assets/images/*.svg")
    
    if not svg_files:
        print("No se encontraron archivos SVG en assets/images")
        return
    
    print(f"Encontrados {len(svg_files)} archivos SVG para convertir")
    
    # Convertir cada archivo SVG a PNG
    success_count = 0
    for svg_path in svg_files:
        png_path = svg_path.replace(".svg", ".png")
        
        if convert_svg_to_png(svg_path, png_path):
            success_count += 1
            print(f"Convertido: {svg_path} -> {png_path}")
        else:
            print(f"Error al convertir {svg_path}")
    
    print(f"Conversión completada. {success_count}/{len(svg_files)} archivos convertidos exitosamente.")

if __name__ == "__main__":
    # Inicializar pygame (necesario para algunas operaciones)
    pygame.init()
    
    # Convertir archivos
    convert_all_svg_to_png()
    
    print("Proceso finalizado") 