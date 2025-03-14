"""
Utilidades para cargar imágenes, incluyendo SVG
"""
import os
import pygame
import io

def load_image(file_path, size=None):
    """
    Carga una imagen desde un archivo, con soporte para SVG.
    
    Args:
        file_path (str): Ruta al archivo de imagen (PNG o SVG)
        size (tuple, optional): Tamaño al que escalar la imagen (ancho, alto)
        
    Returns:
        pygame.Surface: La imagen cargada, o una superficie de color sólido si falla
    """
    sprite = None
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"El archivo no existe: {file_path}")
        return create_fallback_surface(size or (32, 32))
    
    # Determinar el tipo de archivo
    is_svg = file_path.lower().endswith('.svg')
    
    try:
        # Método 1: Intentar cargar directamente con pygame
        sprite = pygame.image.load(file_path)
        
        # Escalar si es necesario
        if size:
            sprite = pygame.transform.scale(sprite, size)
            
        return sprite
    except pygame.error as e:
        # Si falla la carga directa y es un SVG, intentar con cairosvg
        if is_svg:
            try:
                # Método 2: Usar cairosvg si está disponible
                try:
                    import cairosvg
                    png_bytes = cairosvg.svg2png(url=file_path)
                    byte_io = io.BytesIO(png_bytes)
                    sprite = pygame.image.load(byte_io)
                    
                    # Escalar si es necesario
                    if size:
                        sprite = pygame.transform.scale(sprite, size)
                        
                    return sprite
                except (ImportError, ModuleNotFoundError):
                    print(f"No se pudo cargar cairosvg para convertir {file_path}")
            except Exception as e:
                print(f"Error al convertir SVG: {e}")
    
    # Si todo falla, crear una superficie de color sólido
    print(f"No se pudo cargar la imagen: {file_path}")
    return create_fallback_surface(size or (32, 32))

def create_fallback_surface(size, color=(255, 0, 255)):
    """Crea una superficie de color sólido como respaldo"""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface

def convert_svg_to_png(svg_path, png_path=None, size=None):
    """
    Convierte un archivo SVG a PNG
    
    Args:
        svg_path (str): Ruta al archivo SVG
        png_path (str, optional): Ruta donde guardar el PNG. Si es None, se usa la misma ruta con extensión .png
        size (tuple, optional): Tamaño al que escalar la imagen (ancho, alto)
        
    Returns:
        bool: True si la conversión fue exitosa, False en caso contrario
    """
    if not os.path.exists(svg_path):
        print(f"El archivo SVG no existe: {svg_path}")
        return False
    
    if png_path is None:
        png_path = svg_path.replace('.svg', '.png')
    
    try:
        # Intentar usar cairosvg
        try:
            import cairosvg
            if size:
                cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size[0], output_height=size[1])
            else:
                cairosvg.svg2png(url=svg_path, write_to=png_path)
            return True
        except (ImportError, ModuleNotFoundError):
            print("No se pudo cargar cairosvg para convertir SVG a PNG")
            
            # Alternativa: Cargar con pygame y guardar como PNG
            try:
                surface = pygame.image.load(svg_path)
                if size:
                    surface = pygame.transform.scale(surface, size)
                pygame.image.save(surface, png_path)
                return True
            except pygame.error as e:
                print(f"Error al cargar SVG con pygame: {e}")
    except Exception as e:
        print(f"Error al convertir SVG a PNG: {e}")
    
    return False 