import pygame
import Personajes
import clases_p1
import re

def mapa(matriz, ancho, alto, surf):
    x = 0
    y = 0
    for r in matriz:
        for c in r:
            if c == "0":
                muro_rect = rects(x, y, muroN)
                screen.blit(muroN, muro_rect)
            elif c == "x":
                fog_rect = rects(x, y, fogN)
                screen.blit(fogN, fog_rect)
            elif c == "1":
                road_rect = rects(x, y, roadN)
                screen.blit(roadN, road_rect)
            elif c == "2":
                swamp_rect = rects(x, y, swampN)
                screen.blit(swampN, swamp_rect)
            elif c == "3":
                snow_rect = rects(x, y, snowN)
                screen.blit(snowN, snow_rect)
            elif c == "4":
                grass_rect = rects(x, y, grassN)
                screen.blit(grassN, grass_rect)
            elif c == "5":
                water_rect = rects(x, y, waterN)
                screen.blit(waterN, water_rect)
            elif c == "6":
                mountain_rect = rects(x, y, mountainN)
                screen.blit(mountainN, mountain_rect)
            elif c == "@":
                per_rect = rects(x, y, surf)
                screen.blit(surf, per_rect)
            elif c == "7":
                sand_rect = rects(x, y, sandN)
                screen.blit(sandN, sand_rect)

            elif c == "v":
                visi_rect = rects(x, y, visitadoN)
                screen.blit(visitadoN, visi_rect)

            x += ancho / 15
        x = 0
        y += alto / 15

def rects(posx,posy,imagen):
    muro_rect = imagen.get_rect(topleft = (posx,posy))
    return muro_rect

def movimiento(arr_desc, posy, posx):
    arr_desc[posx][posy] = "@"
    if posx != 0:
        if arr_desc[posx - 1][posy] == "v":
            arr_desc[posx - 1][posy] = arr_desc[posx - 1][posy]
        else:
            arr_desc[posx - 1][posy] = laberinto[posx - 1][posy]
    if posy != 0:
        if arr_desc[posx][posy - 1] == "v":
            arr_desc[posx][posy - 1] = arr_desc[posx][posy - 1]
        else:
            arr_desc[posx][posy - 1] = laberinto[posx][posy - 1]

    if posx + 1 != size:
        if arr_desc[posx + 1][posy] == "v":
            arr_desc[posx + 1][posy] = arr_desc[posx + 1][posy]
        else:
            arr_desc[posx + 1][posy] = laberinto[posx + 1][posy]

    if posy + 1 != size:
        if arr_desc[posx][posy + 1] == "v":
            arr_desc[posx][posy + 1] = arr_desc[posx][posy + 1]
        else:
            arr_desc[posx][posy + 1] = laberinto[posx][posy + 1]
    return arr_desc


# funcion para marcar las casillas visitadas, solo cambia la posicion por una v
def marcarVisitado(arr_desc, posy, posx):
    arr_desc[posx][posy] = "v"
    return arr_desc

class TreeNode:
    def __init__(self, posx, posy, g, h, direccion, padre):
        self.posx = posx
        self.posy = posy
        self.g = int(g)
        self.h = int(h)
        self.t = g + h
        self.direccion = direccion
        self.children = []
        self.parent = None
        self.padre = padre

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


def get_neighbors(laberinto, node, final, personaje, closed_list):
    neighbors = []
    rows= 15 
    cols = 15

    # Si tiene un nodo arriba
    if node.posx > 0 and laberinto[node.posx - 1][node.posy] in personaje.terr_disp and laberinto[node.posx - 1][node.posy] not in closed_list:
        nuevo = TreeNode(node.posx - 1, node.posy,g=personaje.pesos[int(laberinto[node.posx-1][node.posy])], h=heuristic(node, final), direccion=None, padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

    # Si tiene un nodo Izquierda
    if node.posy > 0 and laberinto[node.posx][node.posy - 1] in personaje.terr_disp and laberinto[node.posx][node.posy - 1] not in closed_list:
        nuevo = TreeNode(node.posx, node.posy - 1,
                         g=personaje.pesos[int(laberinto[node.posx][node.posy-1])], h=heuristic(node, final), direccion=None, padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

   # Tiene un nodo abajo
    if node.posx < rows - 1 and laberinto[node.posx + 1][node.posy] in personaje.terr_disp and laberinto[node.posx + 1][node.posy] not in closed_list:
        nuevo = TreeNode(node.posx + 1, node.posy,
                         g=personaje.pesos[int(laberinto[node.posx+1][node.posy])], h=heuristic(node, final), direccion=None, padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

    # Si tiene un nodo Derecha
    if node.posy < cols - 1 and laberinto[node.posx][node.posy + 1] in personaje.terr_disp and laberinto[node.posx][node.posy + 1] not in closed_list:
        nuevo = TreeNode(node.posx, node.posy + 1,
                         g=personaje.pesos[int(laberinto[node.posx][node.posy+1])], h=heuristic(node, final), direccion=None, padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

##Esto deberia en vez de ser >0, in personajes.esamadre
    
    return [neighbor for neighbor in neighbors if laberinto[neighbor.posx][neighbor.posy] in personaje.terr_disp]


def heuristic(node, end_node):
    return abs(node.posx - end_node.posx) + abs(node.posy - end_node.posy)


def a_star(laberinto, root, final, personaje):

    ## Esto deberia ir con nodos, si ya tenemos root
    root
    end_node = final

    open_list = [root]
    visitas = [[root.posx,root.posy]]
    closed_list = []
    visitados = []

    while open_list:
        pygame.time.delay(500)
        nodo_actual = min(open_list, key=lambda node: node.g + node.h)
        visitas.remove([nodo_actual.posx,nodo_actual.posy])
        open_list.remove(nodo_actual)
        closed_list.append(nodo_actual)
        visitados.append([nodo_actual.posx,nodo_actual.posy])
        print(str(nodo_actual.posx) + "_ " + str(nodo_actual.posy))

        ##Creo esto debe ser modificado
        if (nodo_actual.posx, nodo_actual.posy) == (final.posx, final.posy):
            print("Si sirvio")
            path = []
            while nodo_actual:
                path.append((nodo_actual.posx, nodo_actual.posy))
                nodo_actual = nodo_actual.padre
            return path[::-1]

        neighbors = get_neighbors(laberinto, nodo_actual, final, personaje, closed_list)
       
        for neighbor in neighbors:
            coords = [neighbor.posx, neighbor.posy]
            if coords in visitados:
                print("Mori")
                continue

            g = nodo_actual.t + int(laberinto[neighbor.posx][neighbor.posy])
            h = heuristic(neighbor, end_node)
            f = g + h

            if neighbor not in open_list or f < neighbor.g + neighbor.h or ([neighbor.posx, neighbor.posy]) not in visitas:
                movimiento(arr_desc,neighbor.posy,neighbor.posx)
                actualizarMapa(arr_desc,charN)
                print("Yep")
                neighbor.g = g
                neighbor.h = h
                neighbor.padre = nodo_actual
                if neighbor not in open_list:
                    open_list.append(neighbor)
                    visitas.append([neighbor.posx,neighbor.posy])

    return None
    

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Laberinto')

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

print(personaje.nombre)
cont = 1
laberinto = []
arr_desc = []
posx = 1
posy = 1
direccion = 'O'
ancho = 800
alto = 800
negro=(0,0,0)
xdd = (ancho/15, alto/15)
objetivox = 13
objetivoy = 7

mannhattan_ini = abs(posx - objetivox) + abs(posy - objetivoy)


muro_surf = pygame.image.load('muro.png').convert_alpha()
muroN = pygame.transform.scale(muro_surf, xdd)

fog_surf = pygame.image.load('graphics/water/0.png').convert_alpha()
fogN = pygame.transform.scale(fog_surf, xdd)

swamp_surf = pygame.image.load('swamp.png').convert_alpha()
swampN = pygame.transform.scale(swamp_surf, xdd)

snow_surf = pygame.image.load('snow.png').convert_alpha()
snowN = pygame.transform.scale(snow_surf, xdd)

grass_surf = pygame.image.load('Grass.png').convert_alpha()
grassN = pygame.transform.scale(grass_surf, xdd)

road_surf = pygame.image.load('Road.png').convert_alpha()
roadN = pygame.transform.scale(road_surf, xdd)

water_surf = pygame.image.load('water.png').convert_alpha()
waterN = pygame.transform.scale(water_surf, xdd)

mountain_surf = pygame.image.load('mountains.png').convert_alpha()
mountainN = pygame.transform.scale(mountain_surf, xdd)

char_surf = pygame.image.load('graphics/character/down/0.png').convert_alpha()
charN = pygame.transform.scale(char_surf, xdd)

octo_surf = pygame.image.load('menu_items/pulpo.png').convert_alpha()
octoN = pygame.transform.scale(octo_surf, xdd)

mono_surf = pygame.image.load('menu_items/mono.png').convert_alpha()
monoN = pygame.transform.scale(mono_surf, xdd)

pg_surf = pygame.image.load('menu_items/pie_grande.png').convert_alpha()
pgN = pygame.transform.scale(pg_surf, xdd)

visitado_surf = pygame.image.load('graphics/soil_water/0.png').convert_alpha()
visitadoN = pygame.transform.scale(visitado_surf, xdd)

sand_surf = pygame.image.load('graphics/soil/rm.png').convert_alpha()
sandN = pygame.transform.scale(sand_surf, xdd)


with open('laberinto.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        x = re.split(r',|\n', line)
        laberinto.insert(cont, x)
        arr_desc.insert(cont, ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"])
        cont = cont + 1

size = len(arr_desc)

def crearArrayInicio(arr_desc, posx,posy):
    arr_desc[posx][posy] = "@"
    if posx != 0:
        arr_desc[posx - 1][posy] = laberinto[posx - 1][posy]
    if posy != 0:
        arr_desc[posx][posy - 1] = laberinto[posx][posy - 1]
    if posx + 1 != size:
        arr_desc[posx + 1][posy] = laberinto[posx + 1][posy]
    if posy + 1 != size:
        arr_desc[posx][posy + 1] = laberinto[posx][posy + 1]
    return arr_desc


# declaracion de la vision inicial del agente y su posicion
arr_desc = crearArrayInicio(arr_desc,posx,posy)

def actualizarMapa(arr_desc, charN):
    '''if clases_p1.humano == True:
        mapa(arr_desc, ancho, alto, charN)
    elif clases_p1.pulpo == True:
        mapa(arr_desc, ancho, alto, octoN)
    elif clases_p1.mono == True:
        mapa(arr_desc,ancho, alto, monoN)
    elif clases_p1.PG == True:
        mapa(arr_desc, ancho, alto, pgN)'''
    mapa(arr_desc, ancho, alto, charN)
    pygame.display.update()
    screen.fill((0, 0, 0))

final = TreeNode(objetivox, objetivoy,
                 personaje.pesos[int(laberinto[objetivox][objetivoy])], 0, direccion, None)

root = TreeNode(posx, posy, 0, mannhattan_ini, direccion, None)

print("\n\n\n\n")

path_a = a_star(laberinto, root, final,personaje)

for i in path_a:
    print(i)

