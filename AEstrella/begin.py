import pygame
import numpy
from sys import exit
from array import *
import re

posiciones = list()
# creacion del mapa
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
            elif c == "7":
                sand_rect = rects(x, y, sandN)
                screen.blit(sandN, sand_rect)
            elif c == "@":
                per_rect = rects(x, y, surf)
                screen.blit(surf, per_rect)


            x += ancho / 15
        x = 0
        y += alto / 15


# movimiento hacia cada direccion y marca con una v las casillas por las que acaba de pasar
def mov_derecha(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    return arr_desc


def mov_izquierda(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    return arr_desc


def mov_arriba(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    return arr_desc


def mov_abajo(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    return arr_desc


# movimiento general
# si encuentra alguna casilla marcada con la v (visitado) entonces la deja asi
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


# rectangulos de las imagenes
def rects(posx, posy, imagen):
    muro_rect = imagen.get_rect(topleft=(posx, posy))
    return muro_rect


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Laberinto')
cont = 1
laberinto = []
arr_desc = []
posx = 1
posy = 1
ancho = 800
alto = 800
negro = (0, 0, 0)
xdd = (ancho / 15, alto / 15)
menuPer = (300, 300)

# se cargan las imagenes y se ponen de un tama;o simetrico a la pantalla y el tama;o de la matriz
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

sand_surf = pygame.image.load('graphics/soil/rm.png').convert_alpha()
sandN = pygame.transform.scale(sand_surf, xdd)

char_surf = pygame.image.load('inicio.png').convert_alpha()
charN = pygame.transform.scale(char_surf, xdd)

fin_surf = pygame.image.load('final.png').convert_alpha()
finN = pygame.transform.scale(fin_surf, xdd)


# lectura del archivo de texto
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

# declaracion de la vision inicial del agente y su posicion
arr_desc[posx][posy] = "@"
for x in range(len(laberinto)):
    for y in range(len(laberinto)):
        arr_desc[x][y] = laberinto [x][y]
# Variables que indican cual agente se activa
humano = True
fin = False

# clase humano con su movimiento
class Humano():
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def movderecha(self, arr_desc, posx, posy):
        if posy + 1 == size:
            return posy
        elif event.key == pygame.K_d and arr_desc[posx][posy + 1] in ("0", "1", "2", "3", "4", "5", "6", "7", "v"):
            posy = posy + 1
            mov_derecha(arr_desc, posy, posx)
        return posy

    def movizquierda(self, arr_desc, posx, posy):
        if posy == 0:
            return posy
        elif event.key == pygame.K_a and arr_desc[posx][posy - 1] in ("0", "1", "2", "3", "4", "5", "6", "7", "v"):
            posy = posy - 1
            mov_izquierda(arr_desc, posy, posx)
        return posy

    def movarriba(self, arr_desc, posx, posy):
        if posx == 0:
            return posx
        elif event.key == pygame.K_w and arr_desc[posx - 1][posy] in ("0", "1", "2", "3", "4", "5", "6", "7", "v"):
            posx = posx - 1
            mov_arriba(arr_desc, posy, posx)
        return posx

    def movabajo(self, arr_desc, posx, posy):
        if posx + 1 == size:
            return posx
        elif event.key == pygame.K_s and arr_desc[posx + 1][posy] in ("0", "1", "2", "3", "4", "5", "6", "7", "v"):
            posx = posx + 1
            mov_abajo(arr_desc, posy, posx)
        return posx

    # creo que no sirve para nada, como yo :-(




band = True
humanoo = Humano(posx, posy)
finn = Humano(posx, posy)
while band == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if laberinto[posx][posy] != "0":
                    posiciones.append((posx, posy))
                    humano = False
                    fin = True
                    if len(posiciones) == 2:
                        band = False
                        pygame.quit()
                else:
                    print("Posición no valida, escoge otra")

            if humano:
                posy = humanoo.movderecha(arr_desc, posx, posy)
                posy = humanoo.movizquierda(arr_desc, posx, posy)
                posx = humanoo.movarriba(arr_desc, posx, posy)
                posx = humanoo.movabajo(arr_desc, posx, posy)
            if fin:
                posy = finn.movderecha(arr_desc, posx, posy)
                posy = finn.movizquierda(arr_desc, posx, posy)
                posx = finn.movarriba(arr_desc, posx, posy)
                posx = finn.movabajo(arr_desc, posx, posy)

    # esto ira actualizando el mapa en cada frame y pondra la imagen del agente que este activado
    if len(posiciones) != 2:
        if humano:
            mapa(arr_desc, ancho, alto, charN)
        if fin:
            mapa(arr_desc, ancho, alto,finN)
        pygame.display.update()
        clock.tick(60)
# pygame.init()
# screen = pygame.display.set_mode((800, 400))
# pygame.display.set_caption('Runner')
