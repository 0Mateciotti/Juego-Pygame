import pygame
from disparo import *
import random

class Nave:

    def __init__(self,imagen:str,posicion:list,ancho,alto,puntos = 0,velocidad = 5,vida = 3,cant_disparos = 4):
        #CONSTRUCTOR NAVE
        #ATRIBUTOS: IMAGEN,POSICION,ANCHO,LARGO
        #ATRIBUTOS CON VALOR POR DEFECTO: PUNTOS,VELOCIDAD VIDA Y CANTIDAD DISPAROS
        self.__imagen = imagen
        self.__posicion = posicion
        self.__rect = ""
        self.__ancho = ancho
        self.__alto = alto
        self.__puntos = puntos
        self.__velocidad = velocidad
        self.__vida = vida
        self.__cant_disparos = cant_disparos

        self.rect = pygame.Rect((self.posicion[0], self.posicion[1], self.ancho, self.alto))
        self.rect.topleft = self.posicion

    def __del__(self):
        print("Muerto")

    #~~~~~~~~~~~~~~~GETTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @property
    def posicion(self):
        return self.__posicion

    @property
    def puntos(self):
        return self.__puntos

    @property
    def velocidad(self):
        return self.__velocidad

    @property
    def vida(self):
        return self.__vida

    @property
    def imagen(self):
        return self.__imagen

    @property
    def rect(self):
        return self.__rect

    @property
    def ancho(self):
        return self.__ancho

    @property
    def alto(self):
        return self.__alto

    @property
    def cant_disparos(self):
        return self.__cant_disparos

    #~~~~~~~~~~~~~SETTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @posicion.setter
    def posicion(self,posicion):
        self.__posicion = posicion

    @puntos.setter
    def puntos(self,puntos):
        self.__puntos = puntos

    @velocidad.setter
    def velocidad(self,velocidad):
        self.__velocidad = velocidad

    @vida.setter
    def vida(self,vida):
        self.__vida = vida

    @rect.setter
    def rect(self,rect):
        self.__rect = rect

    @cant_disparos.setter
    def cant_disparos(self,cant_disparos):
        self.__cant_disparos = cant_disparos

    #~~~~~~~~~~~~~~~~~~~~~~~~METODOS~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def crear_nave(self):
        #USA UNA URL DE UNA IMAGEN, LA CARGA Y ESCALA
        imagen = pygame.image.load(self.__imagen)
        imagen = pygame.transform.scale(imagen,(self.__ancho, self.__alto))

        self.__imagen = imagen
        self.rect = pygame.Rect((self.posicion[0], self.posicion[1], self.ancho, self.alto))



    def mover_nave(self,ancho,lista_teclas):
        #DETECTA LA PULSACION DE CIERTAS TECLAS Y EJECUTA LAS FUNCIONES VINCULADAS A CADA UNA

        self.rect.x = self.posicion[0]
        self.rect.y = self.posicion[1]

        if lista_teclas[pygame.K_RIGHT] and self.posicion[0] < ancho - 75:
            self.posicion[0] = self.posicion[0] + 0.75 * self.velocidad

        if lista_teclas[pygame.K_LEFT] and self.posicion[0] > 0:
            self.posicion[0] = self.posicion[0] - 0.75 * self.velocidad

    def sumar_punto(self,puntos):
        #INCREMENTA LA CANTIDAD DE PUNTOS, RECIBE LA CANTIDAD DE PUNTOS A SUMAR
        self.puntos += puntos

    def morir(self):

        self.__del__()


    def mover_enemigo(self,movimiento:int):
        self.posicion[0] += movimiento


def crear_disparo(img_disparo:str,posicion:list):
    #FUNCIONAMIENTO: CREA UNA INSTANCIA DEL OBJETO DISPARO Y LA RETORNA
    #RECIBE:
    #IMG_DISPARO(TIPO STRING)
    #POSICION(TIPO LISTA)
    disparo = Disparo(img_disparo,(posicion[0]+25,posicion[1]))
    print("Disparo")

    return disparo



