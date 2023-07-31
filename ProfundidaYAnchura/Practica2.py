import pygame
import clases_p1
import begin
import re
from collections import deque


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
            elif c == "v":
                visi_rect = rects(x, y, visitadoN)
                screen.blit(visitadoN, visi_rect)

            x += ancho / 15
        x = 0
        y += alto / 15



# movimiento hacia cada direccion y marca con una v las casillas por las que acaba de pasar
def mov_derecha(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    marcarVisitado(arr_desc, posy - 1, posx)
    return arr_desc


def mov_izquierda(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    marcarVisitado(arr_desc, posy + 1, posx)
    return arr_desc


def mov_arriba(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    marcarVisitado(arr_desc, posy, posx + 1)
    return arr_desc


def mov_abajo(arr_desc, posy, posx):
    movimiento(arr_desc, posy, posx)
    marcarVisitado(arr_desc, posy, posx - 1)
    return arr_desc

cont = 1
laberinto = []
arr_desc = []

posx = begin.posiciones[0][0]
posy = begin.posiciones[0][1]
objetivox = begin.posiciones[1][0]
objetivoy = begin.posiciones[1][1]
ancho = 800
alto = 800

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



# def menuPrincipal(humano_surf, mono_Surf):


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

# for r in laberinto:
#  for c in r:
#    print(c,end = " ")
# print()


# for r in arr_desc:
#  for c in r:
#    print(c,end = " ")
# print()

# tama;o del array
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




# Variables que indican cual agente se activa
humano = clases_p1.humano
mono = clases_p1.mono
sas = clases_p1.PG
ocot = clases_p1.pulpo
costoTotal = 0


class Humano():
    def __init__(self, posx, posy, costoTotal):
        self.posx = posx
        self.posy = posy
        self.costoTotal = costoTotal

    def movderecha(self, arr_desc, posx, posy):
        if posy + 1 == size:
            return False
        elif arr_desc[posx][posy + 1] in ("1", "2", "3", "4", "5", "7", "v"):
            posy = posy + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movizquierda(self, arr_desc, posx, posy):
        if posy == 0:
            return False
        elif arr_desc[posx][posy - 1] in ("1", "2", "3", "4", "5", "7", "v"):
            posy = posy - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movarriba(self, arr_desc, posx, posy):
        if posx == 0:
            return False
        elif arr_desc[posx - 1][posy] in ("1", "2", "3", "4", "5", "7", "v"):
            posx = posx - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movabajo(self, arr_desc, posx, posy):
        if posx + 1 == size:
            return False
        elif arr_desc[posx + 1][posy] in ("1", "2", "3", "4", "5", "7", "v"):
            posx = posx + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False
    
    def calcularCosto(self, arr_desc,posx,posy):
        costo = 0
        if arr_desc[posx][posy] == "1":
            costo += 1
            return costo
        elif arr_desc[posx][posy] == "5":
            costo += 2
            return costo
        elif arr_desc[posx][posy] == "7":
            costo += 3
            return costo
        elif arr_desc[posx][posy] == "4":
            costo += 4
            return costo
        elif arr_desc[posx][posy] in ("2","3"):
            costo += 5
            return costo
        else:
            return costo

class Pulpo():
    def __init__(self, posx, posy, costoTotal):
        self.posx = posx
        self.posy = posy
        self.costoTotal = costoTotal

    def movderecha(self, arr_desc, posx, posy):
        if posy + 1 == size:
            return False
        elif arr_desc[posx][posy + 1] in ("1", "2", "4", "5", "v"):
            posy = posy + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movizquierda(self, arr_desc, posx, posy):
        if posy == 0:
            return False
        elif arr_desc[posx][posy - 1] in ("1", "2", "4", "5", "v"):
            posy = posy - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movarriba(self, arr_desc, posx, posy):
        if posx == 0:
            return False
        elif arr_desc[posx - 1][posy] in ("1", "2", "4", "5", "v"):
            posx = posx - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movabajo(self, arr_desc, posx, posy):
        if posx + 1 == size:
            return False
        elif arr_desc[posx + 1][posy] in ("1", "2", "4", "5", "v"):
            posx = posx + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False
    
    def calcularCosto(self, arr_desc,posx,posy):
        costo = 0
        if arr_desc[posx][posy] in ("1", "2"):
            costo += 2
            return costo
        elif arr_desc[posx][posy] == "5":
            costo += 1
            return costo
        elif arr_desc[posx][posy] == "4":
            costo += 3
            return costo
        else:
            return costo

class Mono():
    def __init__(self, posx, posy, costoTotal):
        self.posx = posx
        self.posy = posy
        self.costoTotal = costoTotal

    def movderecha(self, arr_desc, posx, posy):
        if posy + 1 == size:
            return False
        elif arr_desc[posx][posy + 1] in ("1", "2", "4", "5", "7", "v"):
            posy = posy + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movizquierda(self, arr_desc, posx, posy):
        if posy == 0:
            return False
        elif arr_desc[posx][posy - 1] in ("1", "2", "4", "5", "7", "v"):
            posy = posy - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movarriba(self, arr_desc, posx, posy):
        if posx == 0:
            return False
        elif arr_desc[posx - 1][posy] in ("1", "2", "4", "5", "7", "v"):
            posx = posx - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movabajo(self, arr_desc, posx, posy):
        if posx + 1 == size:
            return False
        elif arr_desc[posx + 1][posy] in ("1", "2", "4", "5", "7", "v"):
            posx = posx + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False
    
    def calcularCosto(self, arr_desc,posx,posy):
        costo = 0
        if arr_desc[posx][posy] == "1":
            costo += 2
            return costo
        elif arr_desc[posx][posy] == "5":
            costo += 4
            return costo
        elif arr_desc[posx][posy] == "7":
            costo += 3
            return costo
        elif arr_desc[posx][posy] == "4":
            costo += 1
            return costo
        elif arr_desc[posx][posy] == "2":
            costo += 5
            return costo
        else:
            return costo


class Sas():
    def __init__(self, posx, posy, costoTotal):
        self.posx = posx
        self.posy = posy
        self.costoTotal = costoTotal

    def movderecha(self, arr_desc, posx, posy):
        if posy + 1 == size:
            return False
        elif arr_desc[posx][posy + 1] in ("1", "2", "4", "3", "6", "v"):
            posy = posy + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        else:
            return False

    def movizquierda(self, arr_desc, posx, posy):
        if posy == 0:
            return False
        elif arr_desc[posx][posy - 1] in ("1", "2", "3", "4", "6", "v"):
            posy = posy - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movarriba(self, arr_desc, posx, posy):
        if posx == 0:
            return False
        elif arr_desc[posx - 1][posy] in ("1", "2", "3", "4", "6", "v"):
            posx = posx - 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False

    def movabajo(self, arr_desc, posx, posy):
        if posx + 1 == size:
            return False
        elif arr_desc[posx + 1][posy] in ("1", "2", "3", "4", "6", "v"):
            posx = posx + 1
            costo = self.calcularCosto(arr_desc, posx, posy)
            print("\n\n\n", costo)
            self.costoTotal += costo
            return True
        return False
    
    def calcularCosto(self, arr_desc,posx,posy):
        costo = 0
        if arr_desc[posx][posy] in ("1", "4"):
            costo += 4
            return costo
        elif arr_desc[posx][posy] == "6":
            costo += 15
            return costo
        elif arr_desc[posx][posy] == "2":
            costo += 5
            return costo
        elif arr_desc[posx][posy] == "3":
            costo += 3
            return costo
        else:
            return costo

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
    


def insertarNodos(arr_desc,nodo,posx,posy, listaInsertados):
    if clases_p1.humano:
        if humanoo.movderecha(arr_desc, posx, posy):
            arr1 = [[posx, posy + 1]]
            print(arr1)
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarDer(posx, posy + 1)
                listaInsertados.append(arr1)

            # izquierda
        if humanoo.movizquierda(arr_desc, posx, posy):
            arr1 = [[posx, posy - 1]]
            print(arr1)
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarIzq(posx, posy - 1)
                listaInsertados.append(arr1)

        if humanoo.movabajo(arr_desc, posx, posy):
            arr1 = [[posx + 1, posy]]
            print(arr1)
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarAba(posx + 1, posy)
                listaInsertados.append(arr1)

        if humanoo.movarriba(arr_desc, posx, posy):
            arr1 = [[posx - 1, posy]]
            print(arr1)
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarArr(posx - 1, posy)
                listaInsertados.append(arr1)
    elif clases_p1.pulpo:
        if ocoto.movderecha(arr_desc, posx, posy):
            arr1 = [[posx, posy + 1]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarDer(posx, posy + 1)
                listaInsertados.append(arr1)

            # izquierda
        if ocoto.movizquierda(arr_desc, posx, posy):
            arr1 = [[posx, posy - 1]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarIzq(posx, posy - 1)
                listaInsertados.append(arr1)

        if ocoto.movabajo(arr_desc, posx, posy):
            arr1 = [[posx + 1, posy]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarAba(posx + 1, posy)
                listaInsertados.append(arr1)

        if ocoto.movarriba(arr_desc, posx, posy):
            arr1 = [[posx - 1, posy]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarArr(posx - 1, posy)
                listaInsertados.append(arr1)
    elif clases_p1.mono:
        if monoo.movderecha(arr_desc, posx, posy):
            arr1 = [[posx, posy + 1]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarDer(posx, posy + 1)
                listaInsertados.append(arr1)

            # izquierda
        if monoo.movizquierda(arr_desc, posx, posy):
            arr1 = [[posx, posy - 1]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarIzq(posx, posy - 1)
                listaInsertados.append(arr1)

        if monoo.movabajo(arr_desc, posx, posy):
            arr1 = [[posx + 1, posy]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarAba(posx + 1, posy)
                listaInsertados.append(arr1)

        if monoo.movarriba(arr_desc, posx, posy):
            arr1 = [[posx - 1, posy]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarArr(posx - 1, posy)
                listaInsertados.append(arr1)
    elif clases_p1.PG:
        print(posy)
        if pg.movderecha(arr_desc,posx,posy):
            arr1 = [[posx, posy + 1]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarDer(posx, posy + 1)
                listaInsertados.append(arr1)

            # izquierda
        if pg.movizquierda(arr_desc, posx, posy):
            arr1 = [[posx, posy - 1]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarIzq(posx, posy - 1)
                listaInsertados.append(arr1)

        if pg.movabajo(arr_desc,posx,posy):
            arr1 = [[posx + 1, posy]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarAba(posx + 1, posy)
                listaInsertados.append(arr1)

        if pg.movarriba(arr_desc,posx,posy):
            arr1 = [[posx - 1, posy]]
            if verificarInsertados(arr1, listaInsertados):
                nodo._insertarArr(posx - 1, posy)
                listaInsertados.append(arr1)
    
    return nodo

def depthSearch(nodo,posx,posy, visitados, listaInsertados,arr_desc,objetivox,objetivoy,stack,anteriorx, anteriory):
    pygame.time.delay(500)
    if nodo.posx == objetivox and nodo.posy == objetivoy:
        movimiento(arr_desc,nodo.posy,nodo.posx)
        marcarVisitado(arr_desc, anteriory,anteriorx)
        anteriorx = nodo.posx
        anteriory = nodo.posy
        actualizarMapa(arr_desc,charN)
        print("Llegaste al final")
        return nodo
    visitados.append(nodo)
    movimiento(arr_desc,nodo.posy,nodo.posx)
    marcarVisitado(arr_desc, anteriory,anteriorx)
    anteriorx = nodo.posx
    anteriory = nodo.posy
    actualizarMapa(arr_desc,charN)
    insertarNodos(arr_desc,nodo, posx,posy,listaInsertados)
    stack.pop()
    #La prioridad es D, B, I, A
    if nodo.arriba != None and verificarVisita(nodo.arriba,visitados):
        stack.append(nodo.arriba) 
    if nodo.izquierda != None and verificarVisita(nodo.izquierda,visitados):
        stack.append(nodo.izquierda)
    if nodo.abajo != None and verificarVisita(nodo.abajo,visitados):
        stack.append(nodo.abajo)
    if nodo.derecha != None and verificarVisita(nodo.derecha,visitados):
        stack.append(nodo.derecha)

    if len(stack) == 0:
        print("No hay solucion")
        return nodo

    depthSearch(stack[-1],stack[-1].posx,stack[-1].posy,visitados,listaInsertados,arr_desc,objetivox,objetivoy,stack,anteriorx, anteriory)    
    

def breadthSearch(nodo,posx,posy, visitados, arr_desc, listaInsertados,objetivox,objetivoy,q, anteriorx, anteriory):
    pygame.time.delay(500)
    if nodo.posx == objetivox and nodo.posy == objetivoy:
        movimiento(arr_desc,nodo.posy,nodo.posx)
        marcarVisitado(arr_desc, anteriory,anteriorx)
        anteriorx = nodo.posx
        anteriory = nodo.posy
        actualizarMapa(arr_desc,charN)
        print("Llegaste al final")
        return nodo
    visitados.append(nodo)
    movimiento(arr_desc,q[0].posy,q[0].posx)
    marcarVisitado(arr_desc, anteriory,anteriorx)
    anteriorx = nodo.posx
    anteriory = nodo.posy
    actualizarMapa(arr_desc,charN)
    insertarNodos(arr_desc,nodo, posx,posy,listaInsertados)
    q.popleft()
    
    if nodo.derecha != None and verificarVisita(nodo.derecha,visitados):
        q.append(nodo.derecha)
    if nodo.abajo != None and verificarVisita(nodo.abajo,visitados):
        q.append(nodo.abajo)
    if nodo.izquierda != None and verificarVisita(nodo.izquierda,visitados):
        q.append(nodo.izquierda)
    if nodo.arriba != None and verificarVisita(nodo.arriba,visitados):
        q.append(nodo.arriba) 
    
    if len(q) == 0:
        print("No hay solucion")
        return nodo

    breadthSearch(q[0],q[0].posx,q[0].posy,visitados,arr_desc,listaInsertados,objetivox,objetivoy,q, anteriorx, anteriory) 
    

def verificarInsertados(array1, listaInsertados):
    if array1 in listaInsertados:
        return False
    return True

def verificarVisita(nodo, visitados):
    for c in visitados:
        if c.posx == nodo.posx and c.posy == nodo.posy:
            return False
    return True



arbol = ArbolBinario(posx,posy)
visitados = []
arr1 = [[posx,posy]]
listaInsertados = []
listaInsertados.append(arr1)

anteriorx = posx
anteriory = posy

q = deque()
q.append(arbol)
qMov = deque()
qMov.append(movimiento(arr_desc,posy,posx))
stack = deque()
stack.append(arbol)
sMov = deque()
sMov.append(movimiento(arr_desc,posy,posx))


def actualizarMapa(arr_desc, charN):
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

humanoo = Humano(posx, posy, costoTotal)
ocoto = Pulpo(posx, posy, costoTotal)
monoo = Mono(posx, posy,costoTotal)
pg = Sas(posx, posy,costoTotal)

def imprimir_arbol(nodo):
    nivel_actual = [nodo]
    while nivel_actual:
        # Imprimimos los datos de cada nodo en el nivel actual
        for nodo in nivel_actual:
            print(f"[{nodo.posx}, {nodo.posy}]", end=" ")
            print("")  # Imprimimos un salto de línea al final del nivel
        # Generamos la lista de nodos del siguiente nivel
        nivel_siguiente = []
        for nodo in nivel_actual:
            # Agregamos los hijos del nodo actual a una lista temporal
            hijos = []
            if nodo.izquierda:
                hijos.append(nodo.izquierda)
            if nodo.derecha:
                hijos.append(nodo.derecha)
            if nodo.arriba:
                hijos.append(nodo.arriba)
            if nodo.abajo:
                hijos.append(nodo.abajo)
            # Agregamos los hijos a la lista del siguiente nivel
            nivel_siguiente.extend(hijos)
        # Actualizamos el nivel actual con la lista del siguiente nivel
        nivel_actual = nivel_siguiente


while True:
    opc = input('Ingrese que algoritmo usar\n1.Por profundidad\n2.Por anchura\n')
    if opc in ("1","2"):
        break
    else:
        print("Esa opcion no es parte del sistema, ingrese otra")

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Laberinto')
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


movimiento(arr_desc,posy,posx)
actualizarMapa(arr_desc,charN)
if opc == "1":
    depthSearch(arbol, posx,posy,visitados, listaInsertados,arr_desc,objetivox,objetivoy, stack,anteriorx,anteriory)
elif opc == "2":
    breadthSearch(arbol,posx,posy, visitados, arr_desc, listaInsertados,objetivox,objetivoy,q,anteriorx,anteriory)
imprimir_arbol(arbol)

for r in arr_desc:
   for c in r:
      print(c,end = " ")
   print()
    

