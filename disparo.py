import pygame
class Disparo:
    def __init__(self,imagen,posicion:list,ancho = 15,alto = 15) :
        self.__posicion = list(posicion)
        self.__ancho = ancho
        self.__alto = alto
        self.__imagen = imagen
        self.__rect = pygame.Rect((self.posicion[0], self.posicion[1], self.__ancho, self.__alto))
    def update_posicion(self):

        self.__rect.center = (self.posicion[0],self.posicion[1])


    @property
    def imagen(self):
        return self.__imagen
    @property
    def posicion(self):
        return self.__posicion
    @property
    def rect(self):
        return self.__rect


    @posicion.setter
    def posicion(self,posicion):
        return posicion



    def draw(self,screen,posicion):
        screen.blit(self.imagen,posicion)

