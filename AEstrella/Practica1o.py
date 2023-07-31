import Personajes
import clases_p1

pj = clases_p1.eleccion
personaje = Personajes

if pj == "humano":
    personaje = Personajes.Humano
elif pj == "pulpo":
    personaje = Personajes.Octopus
elif pj == "mono":
    personaje = Personajes.Monkey
elif pj == "PG":
    personaje = Personajes.Sasquatch

print(pj)
print(personaje.nombre)

class TreeNode:
    def __init__(self, posx, posy, g, h, direccion, padre):
        self.posx = posx
        self.posy = posy
        self.g = g
        self.h = h
        self.direccion = direccion
        self.children = []
        self.parent = None
        self.padre = padre

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


def get_neighbors(matrix, node):
    neighbors = []
    rows, cols = matrix.shape

    ##Si tiene un nodo arriba
    if node.posx > 0:
        neighbors.append(TreeNode(node.posx - 1, node.posy,
                         g=float('inf'), h=float('inf'), direccion=None, padre=node))
    
    # Si tiene un nodo Izquierda
    if node.posy > 0:
        neighbors.append(TreeNode(node.posx, node.posy - 1,
                         g=float('inf'), h=float('inf'), direccion=None, padre=node))
    ##Tiene un nodo abajo
    if node.posx < rows - 1:
        neighbors.append(TreeNode(node.posx + 1, node.posy,
                         g=float('inf'), h=float('inf'), direccion=None, padre=node))
        
    # Si tiene un nodo Derecha
    if node.posy < cols - 1:
        neighbors.append(TreeNode(node.posx, node.posy + 1,
                         g=float('inf'), h=float('inf'), direccion=None, padre=node))

    return [neighbor for neighbor in neighbors if matrix[neighbor.posx][neighbor.posy] > 0]


def heuristic(node, end_node):
    return abs(node.posx - end_node.posx) + abs(node.posy - end_node.posy)


def a_star(matrix, start_pos, end_pos):
    start_node = TreeNode(start_pos[0], start_pos[1], g=0, h=heuristic(
        start_pos, end_pos), direccion=None, padre=None)
    end_node = TreeNode(end_pos[0], end_pos[1], g=float(
        'inf'), h=0, direccion=None, padre=None)

    open_list = [start_node]
    closed_list = []

    while open_list:
        current_node = min(open_list, key=lambda node: node.g + node.h)
        open_list.remove(current_node)
        closed_list.append(current_node)

        if (current_node.posx, current_node.posy) == end_pos:
            path = []
            while current_node:
                path.append((current_node.posx, current_node.posy))
                current_node = current_node.padre
            return path[::-1]

        neighbors = get_neighbors(matrix, current_node)
        for neighbor in neighbors:
            if neighbor in closed_list:
                continue

            g = current_node.g + matrix[neighbor.posx][neighbor.posy]
            h = heuristic(neighbor, end_node)
            f = g + h

            if neighbor not in open_list or f < neighbor.g + neighbor.h:
                neighbor.g = g
                neighbor.h = h
                neighbor.padre = current_node
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None
