import pygame
import numpy as np
import Personajes
from sys import exit
from array import *
import Personajes
import clases_p1
import begin


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
        self.hh = 0

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def get_level(self):
        level = 0 
        p = self.parent
        while p :
            p = p.parent
            level += 1
        return level
    
    def print_tree(self):
        print('  '*self.get_level() + '|--', end = '')
        print(str(self.posx) + "," + str(self.posy))
        if self.children:
            for each in self.children:
                each.print_tree()


def get_neighbors(laberinto, node, final, personaje, closed_list):
    neighbors = []
    rows= 15
    cols = 15

    # Si tiene un nodo arriba
    if node.posx > 0 and laberinto[node.posx - 1][node.posy] in personaje.terr_disp and [node.posx - 1,node.posy] not in closed_list:
        nuevo = TreeNode(node.posx - 1, node.posy,g=personaje.pesos[int(laberinto[node.posx-1][node.posy])], h=heuristic(node, final), direccion='u', padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

    # Si tiene un nodo Izquierda
    if node.posy > 0 and laberinto[node.posx][node.posy - 1] in personaje.terr_disp and [node.posx,node.posy - 1] not in closed_list:
        nuevo = TreeNode(node.posx, node.posy - 1,
                         g=personaje.pesos[int(laberinto[node.posx][node.posy-1])], h=heuristic(node, final), direccion='l', padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

   # Tiene un nodo abajo
    if node.posx < rows - 1 and laberinto[node.posx + 1][node.posy] in personaje.terr_disp and [node.posx + 1,node.posy] not in closed_list:
        nuevo = TreeNode(node.posx + 1, node.posy,
                         g=personaje.pesos[int(laberinto[node.posx+1][node.posy])], h=heuristic(node, final), direccion='d', padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

    # Si tiene un nodo Derecha
    if node.posy < cols - 1 and laberinto[node.posx][node.posy + 1] in personaje.terr_disp and [node.posx,node.posy + 1] not in closed_list:
        nuevo = TreeNode(node.posx, node.posy + 1,
                         g=personaje.pesos[int(laberinto[node.posx][node.posy+1])], h=heuristic(node, final), direccion='r', padre=node)
        neighbors.append(nuevo)
        node.add_child(nuevo)

##Esto deberia en vez de ser >0, in personajes.esamadre
    
    return [neighbor for neighbor in neighbors if laberinto[neighbor.posx][neighbor.posy] in personaje.terr_disp]


def heuristic(node, end_node):
    return abs(node.posx - end_node.posx) + abs(node.posy - end_node.posy)


def a_star(laberinto, root, final, personaje,anteriorx,anteriory):

    ## Esto deberia ir con nodos, si ya tenemos root
    root
    end_node = final

    open_list = [root]
    visitas = [[root.posx,root.posy]]
    closed_list = []
    visitados = []
    suma = 0

    while open_list:
        pygame.time.delay(50)
        nodo_actual = min(open_list, key=lambda node: node.g + node.h)
        visitas.remove([nodo_actual.posx,nodo_actual.posy])
        open_list.remove(nodo_actual)
        closed_list.append(nodo_actual)
        visitados.append([nodo_actual.posx,nodo_actual.posy])
        marcarVisitado(arr_desc,anteriory,anteriorx)
        movimiento(arr_desc,nodo_actual.posy,nodo_actual.posx)
        actualizarMapa(arr_desc)
        anteriorx = nodo_actual.posx
        anteriory = nodo_actual.posy
        print(str(nodo_actual.posx) + "_ " + str(nodo_actual.posy))
        ##Creo esto debe ser modificado
        if (nodo_actual.posx, nodo_actual.posy) == (final.posx, final.posy):
            movimiento(arr_desc,nodo_actual.posy,nodo_actual.posx)
            actualizarMapa(arr_desc)
            print("Si sirvio")
            path = []
            while nodo_actual:
                path.append((nodo_actual.posx, nodo_actual.posy, nodo_actual.direccion))
                suma += nodo_actual.hh
                nodo_actual = nodo_actual.padre
            print("La suma de costos fue " + str(suma))
            return path[::-1]

        neighbors = get_neighbors(laberinto, nodo_actual, final, personaje, visitados)
       
        for neighbor in neighbors:
            coords = [neighbor.posx, neighbor.posy]
            if coords in visitados:
                print("Ya lo visite\n*******")
                continue

            g = nodo_actual.t - nodo_actual.h
            h = heuristic(neighbor, end_node)
            f = g + h

            if neighbor not in open_list or f < neighbor.g + neighbor.h or ([neighbor.posx, neighbor.posy]) not in visitas:
                print("Encontre un papu :v\n*****")
                neighbor.g = g
                neighbor.h = h
                neighbor.padre = nodo_actual
                neighbor.hh = f
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
optimo = []
posx = begin.posiciones[0][0]
posy = begin.posiciones[0][1]
direccion = 'O'
ancho = 800
alto = 800
negro=(0,0,0)
xdd = (ancho/15, alto/15)
objetivox = begin.posiciones[1][0]
objetivoy = begin.posiciones[1][1]

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
        x = line.split(",")
        laberinto.insert(cont, x)
        arr_desc.insert(cont, ["x","x","x","x","x","x","x","x","x","x","x","x","x","x","x"])
        optimo.insert(cont, ["x","x","x","x","x","x","x","x","x","x","x","x","x","x","x"])
        cont  = cont+1

#for r in laberinto:
 #  for c in r:
  #    print(c,end = " ")
   #print()


#for r in arr_desc:
 #  for c in r:
  #    print(c,end = " ")
   #print()

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
optimo = crearArrayInicio(optimo,posx,posy)

def actualizarMapa(arr_desc):
    if clases_p1.humano == True:
        mapa(arr_desc, ancho, alto, charN)
    elif clases_p1.pulpo == True:
        mapa(arr_desc, ancho, alto, octoN)
    elif clases_p1.mono == True:
        mapa(arr_desc,ancho, alto, monoN)
    elif clases_p1.PG == True:
        mapa(arr_desc, ancho, alto, pgN)
    pygame.display.update()
    screen.fill((0, 0, 0))

final = TreeNode(objetivox, objetivoy,
                 personaje.pesos[int(laberinto[objetivox][objetivoy])], 0, direccion, None)

root = TreeNode(posx, posy, 0, mannhattan_ini, direccion, None)

print("\n\n\n\n")

movimiento(arr_desc,posy,posx)
actualizarMapa(arr_desc)
anteriorx=posy
anteriory=posx
path_a = a_star(laberinto, root, final,personaje,anteriorx,anteriory)

print("\n\n=================================================\n CAMINO OPTIMO")

for i in range(len(path_a)):
    pygame.time.delay(300)
    marcarVisitado(optimo,anteriory,anteriorx)
    movimiento(optimo,path_a[i][1],path_a[i][0])
    actualizarMapa(optimo)
    anteriorx = path_a[i][0]
    anteriory = path_a[i][1]

for i in path_a:
    print (i)

print()
for r in optimo:
   for c in r:
      print(c,end = " ")
   print()

print("\n\n=================================================\nARBOL GENERADO\n")
root.print_tree()
