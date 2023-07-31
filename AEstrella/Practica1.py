import pygame
import numpy as np
from sys import exit
from array import *


def mapa(matriz, ancho, alto):
    x=0
    y=0
    for r in matriz:
        for c in r:
            if c == "0":
                muro_rect = muro(x,y,muroN)
                screen.blit(muroN,muro_rect)
            elif c == "x":
                fog_rect = fog(x,y,fogN)
                screen.blit(fogN,fog_rect)
            elif c == "1":
                road_rect = road(x,y,roadN)
                screen.blit(roadN,road_rect)
            elif c == "2":
                swamp_rect = road(x,y,swampN)
                screen.blit(swampN,swamp_rect)
            elif c == "3":
                snow_rect = road(x,y,snowN)
                screen.blit(snowN,snow_rect)
            elif c == "4":
                grass_rect = road(x,y,grassN)
                screen.blit(grassN,grass_rect)
            elif c == "5":
                water_rect = road(x,y,waterN)
                screen.blit(waterN,water_rect)
            elif c == "6":
                mountain_rect = road(x,y,mountainN)
                screen.blit(mountainN,mountain_rect)
            elif c == "@":
                per_rect = per(x,y,charN)
                screen.blit(charN,per_rect)


            x+=ancho/15
        x=0
        y += alto/15
    


def muro(posx,posy,imagen):
    muro_rect = imagen.get_rect(topleft = (posx,posy))
    return muro_rect

def fog(posx,posy,imagen):
    fog_rect = imagen.get_rect(topleft = (posx,posy))
    return fog_rect

def per(posx,posy,imagen):
    per_rect = imagen.get_rect(topleft = (posx,posy))
    return per_rect

def swamp(posx,posy,imagen):
    swamp_rect = imagen.get_rect(topleft = (posx,posy))
    return swamp_rect

def grass(posx,posy,imagen):
    grass_rect = imagen.get_rect(topleft = (posx,posy))
    return grass_rect

def road(posx,posy,imagen):
    road_rect = imagen.get_rect(topleft = (posx,posy))
    return road_rect

def snow(posx,posy,imagen):
    snow_rect = imagen.get_rect(topleft = (posx,posy))
    return snow_rect

def water(posx,posy,imagen):
    water_rect = imagen.get_rect(topleft = (posx,posy))
    return water_rect  

def mountain(posx,posy,imagen):
    mountain_rect = imagen.get_rect(topleft = (posx,posy))
    return mountain_rect  

class TreeNode:
    def __init__(self, posx, posy, direccion, padre):
        self.posx = posx
        self.posy = posy
        self.direccion = direccion
        self.children = []
        self.parent = None
        self.padre = padre

    def get_level(self):
        level = 0
        p = self.padre
        while p:
            level += 1
            p = p.padre

        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|" if self.padre else ""
        print(prefix + self.direccion)
        if self.children:
            for child in self.children:
                child.print_tree()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_path_to_leaf(self, leaf):
        path = []
        if self.find_path_to_leaf(leaf, path):
            print("Path to leaf ({}, {}):".format(leaf.posx, leaf.posy))
            print(" -> ".join("({},{} ({}))".format(node.posx, node.posy, node.direccion)
                  for node in path))
        else:
            print("Leaf ({}, {}) not found in the tree.".format(
                leaf.posx, leaf.posy))

    def find_path_to_leaf(self, leaf, path):
        if self is None:
            return False

        path.append(self)

        if self.posx == leaf.posx and self.posy == leaf.posy:
            return True

        for child in self.children:
            if child.find_path_to_leaf(leaf, path):
                return True

        path.pop()
        return False
    
##### RIGHT DOWN LEFT UP#######


def depthSearch(visitados, nodoActual, laberinto, posx, posy, objetivox, objetivoy, found):
    aux = 0
    aux2 = 0
    auy = 0
    auy2 = 0
    print("found vale " + str(found))
    if found == 1:
        return found
    else:
        if posx+1 == 15 or posy+1 == 15:
            return
        print(nodoActual.posx, "\t", nodoActual.posy)
        print("aao" + laberinto[posx][posy+1])
        if nodoActual.posx == objetivox and nodoActual.posy == objetivoy:
            print("FOUUUUNDDD!!")
            found = 1
            return nodoActual
        if laberinto[posx][posy+1] in ("1", "2", "3", "4", "5", "6"):
            print("a")
            nodoSig = TreeNode(posx, posy+1, 'r', nodoActual)
            auy = nodoActual.parent.posy
            auy2 = nodoSig.posy
            aux = nodoActual.parent.posx
            aux2 = nodoSig.posx
            print("Se supone aqui imprimo" + str(aux) + "," +  str(auy) + " y " + str(aux2) +","+ str(auy2))
            if aux == aux2 and auy == auy2:
                print("Aqui SE SUPONE MUERE")
                return
            if nodoActual.parent == nodoSig:
                print("XDDDD")
                return False
            if comprobarVisita(visitados, nodoSig):
                return False
            else:
                nodoActual.add_child(nodoSig)
                visitados.append(nodoSig)
                posy = posy+1
                ##print(nodoSig.posx, "\t", nodoSig.posy)
                resultado = depthSearch(
                    visitados, nodoSig, laberinto, nodoSig.posx, nodoSig.posy, objetivox, objetivoy,found)
                if resultado:
                    return resultado

        if laberinto[posx+1][posy] in ("1", "2", "3", "4", "5", "6"):
            print("a")
            nodoSig = TreeNode(posx+1, posy, 'd', nodoActual)
            auy = nodoActual.parent.posy
            auy2 = nodoSig.posy
            aux = nodoActual.parent.posx
            aux2 = nodoSig.posx
            print("Se supone aqui imprimo" + str(aux) + "," +
                str(auy) + " y " + str(aux2) + "," + str(auy2))
            if aux == aux2 and auy == auy2:
                print("Aqui SE SUPONE MUERE")
                return
            if nodoActual.parent == nodoSig:
                print("XDDDD")
                return False
            if comprobarVisita(visitados, nodoSig):
                return False
            else:
                nodoActual.add_child(nodoSig)
                visitados.append(nodoSig)
                posx = posx + 1
                ##print(nodoSig.posy, "\t", nodoSig.posx)
                resultado = depthSearch(
                    visitados, nodoSig, laberinto, nodoSig.posx, nodoSig.posy, objetivox, objetivoy,found)
                if resultado:
                    return resultado

        if laberinto[posx][posy-1] in ("1", "2", "3", "4", "5", "6"):
            print("a")
            nodoSig = TreeNode(posx, posy-1, 'l', nodoActual)
            auy = nodoActual.parent.posy
            auy2 = nodoSig.posy
            aux = nodoActual.parent.posx
            aux2 = nodoSig.posx
            print("Se supone aqui imprimo" + str(aux) + "," +
                str(auy) + " y " + str(aux2) + "," + str(auy2))
            if aux == aux2 and auy == auy2:
                print("Aqui SE SUPONE MUERE")
                return
            if nodoActual.parent == nodoSig:
                print("XDDDD")
                return False
            if comprobarVisita(visitados, nodoSig):
                return False
            else:
                nodoActual.add_child(nodoSig)
                visitados.append(nodoSig)
                posy = posy - 1
                ##print(nodoSig.posy, "\t", nodoSig.posx)
                resultado = depthSearch(
                    visitados, nodoSig, laberinto, nodoSig.posx, nodoSig.posy, objetivox, objetivoy,found)
                if resultado:
                    return resultado

        if laberinto[posx-1][posy] in ("1", "2", "3", "4", "5", "6"):
            print("a")
            nodoSig = TreeNode(posx-1, posy, 'u', nodoActual)
            auy = nodoActual.parent.posy
            auy2 = nodoSig.posy
            aux = nodoActual.parent.posx
            aux2 = nodoSig.posx
            print("Se supone aqui imprimo" + str(aux) + "," +
                str(auy) + " y " + str(aux2) + "," + str(auy2))
            if aux == aux2 and auy == auy2:
                print("Aqui SE SUPONE MUERE")
                return
            if comprobarVisita(visitados, nodoSig):
                return False
            else:
                nodoActual.add_child(nodoSig)
                visitados.append(nodoSig)
                posx = posx - 1
                ##print(nodoSig.posy, "\t", nodoSig.posx)
                resultado = depthSearch(
                    visitados, nodoSig, laberinto, nodoSig.posx, nodoSig.posy, objetivox, objetivoy,found)
                if resultado:
                    return resultado


def comprobarVisita(visitados, nodo):
    if nodo in visitados:
        return True
    else:
        return False



pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Laberinto')
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
root = TreeNode(posx,posy,direccion, None)
apoyo = TreeNode(posx, posy, direccion, root)
root.add_child(apoyo)
visitados = []
visitados.append(root)
visitados.append(apoyo)
found = 0

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


with open('laberinto.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        x = line.split(",")
        laberinto.insert(cont, x)
        arr_desc. insert(cont, ["x","x","x","x","x","x","x","x","x","x","x","x","x","x","x"])
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


arr_desc[posx][posy] = "@"
arr_desc[posx-1][posy] = laberinto[posx-1][posy]
arr_desc[posx][posy-1] = laberinto[posx][posy-1]
arr_desc[posx+1][posy] = laberinto[posx+1][posy]
arr_desc[posx][posy+1] = laberinto[posx][posy+1]
objetivox = 13
objetivoy = 7


"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and laberinto[posx][posy+1] in  ("1", "2", "3", "4", "5", "6") :
                posy = posy+1
                arr_desc[posx][posy] = "@"
                arr_desc[posx-1][posy] = laberinto[posx-1][posy]
                arr_desc[posx][posy-1] = laberinto[posx][posy-1]
                arr_desc[posx+1][posy] = laberinto[posx+1][posy]
                arr_desc[posx][posy+1] = laberinto[posx][posy+1]
                

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and laberinto[posx][posy-1]  in  ("1", "2", "3", "4", "5", "6"):
                posy = posy-1
                arr_desc[posx][posy] = "@"
                arr_desc[posx-1][posy] = laberinto[posx-1][posy]
                arr_desc[posx][posy-1] = laberinto[posx][posy-1]
                arr_desc[posx+1][posy] = laberinto[posx+1][posy]
                arr_desc[posx][posy+1] = laberinto[posx][posy+1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and laberinto[posx-1][posy]  in  ("1", "2", "3", "4", "5", "6"):
                posx = posx-1
                arr_desc[posx][posy] = "@"
                arr_desc[posx-1][posy] = laberinto[posx-1][posy]
                arr_desc[posx][posy-1] = laberinto[posx][posy-1]
                arr_desc[posx+1][posy] = laberinto[posx+1][posy]
                arr_desc[posx][posy+1] = laberinto[posx][posy+1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and laberinto[posx+1][posy]  in  ("1", "2", "3", "4", "5", "6"):
                posx = posx+1
                arr_desc[posx][posy] = "@"
                arr_desc[posx-1][posy] = laberinto[posx-1][posy]
                arr_desc[posx][posy-1] = laberinto[posx][posy-1]
                arr_desc[posx+1][posy] = laberinto[posx+1][posy]
                arr_desc[posx][posy+1] = laberinto[posx][posy+1]


"""

print("\n\n\n\n")

    ##screen.fill(negro)
    ##mapa(arr_desc,ancho,alto)
    
nodo_objetivo = depthSearch(visitados, apoyo, laberinto, posx, posy, objetivox, objetivoy,found)

root.print_path_to_leaf(nodo_objetivo)


    ##pygame.display.update()
    ##clock.tick(60)
apoyo.print_tree()

#pygame.init()
#screen = pygame.display.set_mode((800, 400))
#pygame.display.set_caption('Runner')
