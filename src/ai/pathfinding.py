

import heapq
from src.utils.constants import TILE_SIZE

class AStar:
    """Implementación del algoritmo A* para encontrar caminos"""
    def __init__(self, level):
        self.level = level
    
    def find_path(self, start_x, start_y, end_x, end_y):
        """
        Encuentra un camino desde (start_x, start_y) hasta (end_x, end_y)
        Retorna una lista de puntos (x, y) que forman el camino
        """
        # Convertir coordenadas de píxeles a coordenadas de cuadrícula
        start = (int(start_x / TILE_SIZE), int(start_y / TILE_SIZE))
        end = (int(end_x / TILE_SIZE), int(end_y / TILE_SIZE))
        
        # Si el inicio o el fin están en un obstáculo, no hay camino
        if self.level.is_tile_blocked(start[0], start[1]) or self.level.is_tile_blocked(end[0], end[1]):
            return []
        
        # Conjunto de nodos visitados
        closed_set = set()
        
        # Conjunto de nodos por visitar (cola de prioridad)
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # Diccionario para reconstruir el camino
        came_from = {}
        
        # Costo desde el inicio hasta cada nodo
        g_score = {start: 0}
        
        # Costo estimado desde el inicio hasta el final pasando por cada nodo
        f_score = {start: self.heuristic(start, end)}
        
        while open_set:
            # Obtener el nodo con menor f_score
            current_f, current = heapq.heappop(open_set)
            
            # Si hemos llegado al destino, reconstruir y devolver el camino
            if current == end:
                return self.reconstruct_path(came_from, current)
            
            # Marcar como visitado
            closed_set.add(current)
            
            # Explorar vecinos
            for neighbor in self.get_neighbors(current):
                # Ignorar vecinos ya visitados
                if neighbor in closed_set:
                    continue
                
                # Calcular g_score tentativo
                tentative_g_score = g_score[current] + 1
                
                # Si el vecino no está en open_set o tiene un mejor g_score
                if neighbor not in [i[1] for i in open_set] or tentative_g_score < g_score.get(neighbor, float('inf')):
                    # Actualizar información del vecino
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, end)
                    
                    # Añadir a open_set si no está ya
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # Si no se encuentra camino, devolver lista vacía
        return []
    
    def heuristic(self, a, b):
        """Heurística de distancia Manhattan"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self, node):
        """Obtiene los vecinos válidos de un nodo"""
        x, y = node
        neighbors = []
        
        # Direcciones: arriba, derecha, abajo, izquierda
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Comprobar si está dentro de los límites del nivel
            if 0 <= nx < self.level.width and 0 <= ny < self.level.height:
                # Comprobar si no hay obstáculo
                if not self.level.is_tile_blocked(nx, ny):
                    neighbors.append((nx, ny))
        
        return neighbors
    
    def reconstruct_path(self, came_from, current):
        """Reconstruye el camino desde el nodo final hasta el inicial"""
        path = []
        while current in came_from:
            # Convertir coordenadas de cuadrícula a píxeles (centro de la casilla)
            path.append((current[0] * TILE_SIZE + TILE_SIZE // 2, 
                         current[1] * TILE_SIZE + TILE_SIZE // 2))
            current = came_from[current]
        
        # Añadir el nodo inicial
        path.append((current[0] * TILE_SIZE + TILE_SIZE // 2, 
                     current[1] * TILE_SIZE + TILE_SIZE // 2))
        
        # Invertir el camino para que vaya desde el inicio hasta el final
        path.reverse()
        
        return path 