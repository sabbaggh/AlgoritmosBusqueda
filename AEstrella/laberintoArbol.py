import pygame
import numpy
from sys import exit
from array import *



#Creacion del mapa de acuerdo a la matriz "desconocida"
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
            elif c == "@":
                per_rect = per(x,y,charN)
                screen.blit(charN,per_rect)
            elif c == "*":
                flag_rect = flag(x,y,flagN)
                screen.blit(flagN,flag_rect)

            x+=ancho/size
        x=0
        y += alto/size
    


#Rectangulos para cada imagen
def muro(posx,posy,imagen):
    muro_rect = imagen.get_rect(topleft = (posx,posy))
    return muro_rect

def fog(posx,posy,imagen):
    fog_rect = imagen.get_rect(topleft = (posx,posy))
    return fog_rect

def per(posx,posy,imagen):
    per_rect = imagen.get_rect(topleft = (posx,posy))
    return per_rect

def flag(posx,posy,imagen):
    flag_rect = imagen.get_rect(topleft = (posx,posy))
    return flag_rect

#movimiento
def mov_derecha(arr_desc,posy,posx):
    arr_desc[posx][posy] = "@"
    arr_desc[posx-1][posy] = laberinto[posx-1][posy]
    arr_desc[posx][posy-1] = laberinto[posx][posy-1]
    arr_desc[posx+1][posy] = laberinto[posx+1][posy]
    arr_desc[posx][posy+1] = laberinto[posx][posy+1]
    return arr_desc

def mov_izquierda(arr_desc,posy,posx):
    arr_desc[posx][posy] = "@"
    arr_desc[posx-1][posy] = laberinto[posx-1][posy]
    arr_desc[posx][posy-1] = laberinto[posx][posy-1]
    arr_desc[posx+1][posy] = laberinto[posx+1][posy]
    arr_desc[posx][posy+1] = laberinto[posx][posy+1]
    return arr_desc

def mov_arriba(arr_desc,posy,posx):
    arr_desc[posx][posy] = "@"
    arr_desc[posx-1][posy] = laberinto[posx-1][posy]
    arr_desc[posx][posy-1] = laberinto[posx][posy-1]
    arr_desc[posx+1][posy] = laberinto[posx+1][posy]
    arr_desc[posx][posy+1] = laberinto[posx][posy+1]
    return arr_desc

def mov_abajo(arr_desc,posy,posx):
    arr_desc[posx][posy] = "@"
    arr_desc[posx-1][posy] = laberinto[posx-1][posy]
    arr_desc[posx][posy-1] = laberinto[posx][posy-1]
    arr_desc[posx+1][posy] = laberinto[posx+1][posy]
    arr_desc[posx][posy+1] = laberinto[posx][posy+1]
    return arr_desc








cont = 0
laberinto = []
arr_desc = []

with open('laberinto.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        x = line.split(",")
        laberinto.insert(cont, x)
        arr_desc. insert(cont, ["x","x","x","x","x","x","x","x","x","x","x","x","x","x","x"])
        cont  = cont+1

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Laberinto')
#posicion inicial del personaje
posx = 1
posy = 1
#tamaño de la pantalla
ancho = 800
alto = 800
fil = 1
col = 1
size = len(arr_desc)
xdd = (ancho/size, alto/size)



#Se cargan las imagenes y se reescalan de acuerdo al tamaño de pantalla y del array para que quede simetrico
muro_surf = pygame.image.load('muro.png').convert_alpha()
muroN = pygame.transform.scale(muro_surf, xdd)
fog_surf = pygame.image.load('graphics/water/0.png').convert_alpha()
fogN = pygame.transform.scale(fog_surf, xdd)
char_surf = pygame.image.load('graphics/character/down/0.png').convert_alpha()
charN = pygame.transform.scale(char_surf, xdd)
flag_surf = pygame.image.load('flag.png').convert_alpha()
flagN = pygame.transform.scale(flag_surf, xdd)




#for r in laberinto:
 #  for c in r:
  #    print(c,end = " ")
   #print()


#for r in arr_desc:
 #  for c in r:
  #    print(c,end = " ")
   #print()




#posicion inicial y sensores del agente
arr_desc[posx][posy] = "@"
arr_desc[posx-1][posy] = laberinto[posx-1][posy]
arr_desc[posx][posy-1] = laberinto[posx][posy-1]
arr_desc[posx+1][posy] = laberinto[posx+1][posy]
arr_desc[posx][posy+1] = laberinto[posx][posy+1]
objetivo = "*"

    

class ArbolBinario():
    def __init__(self,posx,posy):
        self.posx = posx
        self.posy = posy
        self.derecha = None
        self.izquierda = None
        self.abajo = None
        self.arriba = None
    
    def _insertarDer(self, posx,posy):
        if self.derecha is None:
            self.derecha = ArbolBinario(posx,posy)
        else:
            self.derecha._insertarDer(posx,posy)
            

    def _insertarIzq(self, posx,posy):
        if self.izquierda is None:
            self.izquierda = ArbolBinario(posx,posy)
        else:
            self.izquierda._insertarIzq(posx,posy)

    def _insertarAba(self, posx,posy):
        if self.abajo is None:
            self.abajo = ArbolBinario(posx,posy)
        else:
            self.abajo._insertarAba(posx,posy)

    def _insertarArr(self, posx,posy):
        if self.arriba is None:
            self.arriba = ArbolBinario(posx,posy)
        else:
            self.arriba._insertarArr(posx,posy)


def depthSearch(visitados,nodoActual, arr_desc, posx, posy, objetivo):
    pygame.time.delay(500)
    if nodoActual.posx == objetivo and nodoActual.posy == objetivo:
        return nodoActual
    if arr_desc[posx][posy+1] == "1":
        nodoActual._insertarDer(posx,posy+1)
        nodoSig = nodoActual.derecha
        if comprobarVisita(visitados, nodoSig):
            return nodoActual
        else:
            visitados.append(nodoSig)
            posy = posy+1
            print(nodoSig.posy, "\t", nodoSig.posx)
            mov_derecha(arr_desc, posy, posx)
            mapa(arr_desc, ancho, alto)
            pygame.display.update()
            screen.fill((0, 0, 0))
            resultado = depthSearch(visitados,nodoSig, arr_desc, posx, posy, objetivo)
            if resultado:
                return resultado

    elif arr_desc[posx+1][posy] == "1":
        nodoActual._insertarAba(posx+1,posy)
        nodoSig = nodoActual.abajo
        if comprobarVisita(visitados, nodoSig):
            return nodoActual
        else:
            visitados.append(nodoSig)
            posx = posx + 1
            print(nodoSig.posy, "\t", nodoSig.posx)
            mov_abajo(arr_desc, posy, posx)
            mapa(arr_desc, ancho, alto)
            pygame.display.update()
            screen.fill((0, 0, 0))
            resultado = depthSearch(visitados,nodoSig, arr_desc, posx, posy, objetivo)
            if resultado:
                return resultado
        
    elif arr_desc[posx][posy-1] == "1":

        nodoActual._insertarIzq(posx, posy-1)
        nodoSig = nodoActual.izquierda
        if comprobarVisita(visitados, nodoSig):
            return nodoActual
        else:
            visitados.append(nodoSig)
            posy = posy - 1
            print(nodoSig.posy, "\t", nodoSig.posx)
            mov_izquierda(arr_desc, posy, posx)
            mapa(arr_desc, ancho, alto)
            pygame.display.update()
            screen.fill((0, 0, 0))
            resultado = depthSearch(visitados,nodoSig, arr_desc, posx, posy, objetivo)
            if resultado:
                return resultado

    elif arr_desc[posx-1][posy] == "1":
        nodoActual._insertarArr(posx-1, posy)
        nodoSig = nodoActual.arriba
        if comprobarVisita(visitados, nodoSig):
            return nodoActual
        else:
            visitados.append(nodoSig)
            posx = posx - 1
            mov_arriba(arr_desc, posy, posx)
            mapa(arr_desc, ancho, alto)
            pygame.display.update()
            screen.fill((0, 0, 0))
            resultado = depthSearch(visitados,nodoSig, arr_desc, posx, posy, objetivo)
            if resultado:
                return resultado

def comprobarVisita(visitados, nodo):
    for c in visitados:
        if c.posx == nodo.posx and c.posy == nodo.posy:
            return True
        else:
            return False




arbol = ArbolBinario(posx,posy)
visitados = []
visitados.append(arbol)



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and arr_desc[posx][posy+1] == "1":
                posy = posy+1
                mov_derecha(arr_desc, posy, posx)
                

            if event.key == pygame.K_a and arr_desc[posx][posy-1] == "1":
                posy = posy-1
                mov_izquierda(arr_desc,posy,posx)

            if event.key == pygame.K_w and arr_desc[posx-1][posy] == "1":
                posx = posx-1
                mov_arriba(arr_desc,posy,posx)

            if event.key == pygame.K_s and arr_desc[posx+1][posy] == "1":
                posx = posx+1
                mov_abajo(arr_desc,posy,posx)
                
    



    #print(arbol.valor)

    mapa(arr_desc,ancho,alto)
    pygame.display.update()
    screen.fill((0, 0, 0))
    print(arbol.posx)
    depthSearch(visitados,arbol,arr_desc,posx,posy,objetivo)
    clock.tick(60)


#pygame.init()
#screen = pygame.display.set_mode((800, 400))
#pygame.display.set_caption('Runner')
