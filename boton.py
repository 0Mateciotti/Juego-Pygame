import pygame
from funciones_generales import cargar_imagen

class Boton:
    def __init__(self,x,y,imagen1):

        self.x = x
        self.y = y
        self.imagen1 = imagen1
        self.rect = self.imagen1.get_rect()
        self.rect.topleft = (x,y)


