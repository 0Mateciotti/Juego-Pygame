import pygame
from funciones_generales import cargar_imagen

class Boton:
    def __init__(self,x,y,imagen1,imagen2):

        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.rect = self.imagen1.get_rect()
        self.rect.topleft = (x,y)

    def mostar(self,imagen):
        pygame.blit(imagen,(self.rect.x,self.rect.y))
