import pygame
import json
import re
from Nave import Nave
pygame.mixer.init()
def detectar_colicion(rect_1,rect_2) ->bool:
    #FUNCIONALIDAD: SI EL TIPO ES 1, VA A VERIFICAR LA COLICION DEL rect_1 CON LA DEL rect_2. SI EL TIPO ES 0, VA A VERIFICAR LA COLISION DEL PUNTO 1 CON lista_rect

    retorno = 0

    if len(rect_1) != 0 and len(rect_2) != 0 :
        retorno = 1 if rect_1.colliderect(rect_2) == True else 0

    return retorno

def detectar_colicion_lista(rect,lista:list):

    retorno = 1 if rect.collidelist(lista) >= 0 else 0

    return retorno


def parse_puntos(archivo:str,) ->list:
    i = 0
    with open(archivo,'r') as archivo:
        lista_puntos = []
        todo = archivo.read()
        nombre = re.findall(r'"Nombre": "([a-zA-Z0-9]+) ',todo)
        tiempo = re.findall(r'"Tiempo": ([0-9]+)',todo)
        puntos = re.findall(r'"Puntos": ([0-9]+)',todo)

        for i in range(len(nombre)):
            dic_puntaje = {}
            dic_puntaje["Nombre"] = nombre[i]
            dic_puntaje["Tiempo"] = tiempo[i]
            dic_puntaje["Puntos"] = puntos[i]
            lista_puntos.append(dic_puntaje)
            i += 1
    return lista_puntos

def generar_enemigos(enemigos:list,rectangulos_enemigos:list,pos:list,img,cantidad,separacion:int):
    a = pos

    for i in range(cantidad):
        aux = Nave(img,[a[0],a[1]],50,50)
        enemigos.append(aux)
        #rectangulos_enemigos.append(aux.rect)
        a[0] += separacion


def generar_tandas(enemigos:list,rectangulos_enemigos:list,img,tanda:int):
    x_segunda_tanda = 100

    if tanda == 1:
        generar_enemigos(enemigos, rectangulos_enemigos, [100, 100], img, 5, 200)
        generar_enemigos(enemigos, rectangulos_enemigos, [200, 200], img, 4, 200)
        generar_enemigos(enemigos, rectangulos_enemigos, [300, 300], img, 3, 200)
    if tanda > 1:
        for i in range(3):
            generar_enemigos(enemigos, rectangulos_enemigos, [x_segunda_tanda, 100], img, 2, 75)
            generar_enemigos(enemigos, rectangulos_enemigos, [x_segunda_tanda, 200], img, 2, 75)
            generar_enemigos(enemigos, rectangulos_enemigos, [x_segunda_tanda, 300], img, 2, 75)
            generar_enemigos(enemigos, rectangulos_enemigos, [x_segunda_tanda, 400], img, 2, 75)
            x_segunda_tanda += 400

def cargar_imagen(imagen_url,escala:list):
    retorno = pygame.image.load(imagen_url)
    retorno = pygame.transform.scale(retorno,escala)
    return retorno

def cargar_sonido(sonido,volumen):
    retorno = pygame.mixer.Sound(sonido)
    retorno.set_volume(volumen)

    return retorno

