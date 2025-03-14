
class BehaviorTree:
    """Clase principal del árbol de comportamiento"""
    def __init__(self, root_node):
        self.root = root_node
    
    def execute(self, state):
        """Ejecuta el árbol de comportamiento con el estado actual"""
        return self.root.execute(state)

class Node:
    """Clase base para todos los nodos del árbol de comportamiento"""
    def execute(self, state):
        """Método a implementar en las subclases"""
        pass

class Sequence(Node):
    """Ejecuta los nodos hijos en secuencia hasta que uno falle"""
    def __init__(self, children):
        self.children = children
    
    def execute(self, state):
        """Ejecuta todos los nodos hijos en orden. Si alguno falla, retorna False"""
        for child in self.children:
            if not child.execute(state):
                return False
        return True

class Selector(Node):
    """Ejecuta los nodos hijos en secuencia hasta que uno tenga éxito"""
    def __init__(self, children):
        self.children = children
    
    def execute(self, state):
        """Ejecuta los nodos hijos hasta que uno tenga éxito. Si todos fallan, retorna False"""
        for child in self.children:
            if child.execute(state):
                return True
        return False

class Condition(Node):
    """Nodo que evalúa una condición"""
    def __init__(self, condition_func):
        self.condition_func = condition_func
    
    def execute(self, state):
        """Ejecuta la función de condición y retorna su resultado"""
        return self.condition_func(state)

class Action(Node):
    """Nodo que ejecuta una acción"""
    def __init__(self, action_func):
        self.action_func = action_func
    
    def execute(self, state):
        """Ejecuta la función de acción y retorna su resultado"""
        return self.action_func(state) 