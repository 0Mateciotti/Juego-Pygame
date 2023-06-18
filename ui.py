import pygame
import colores

def mostrar_puntuacion(puntuacion:str,screen) -> list:
    fuente = pygame.font.SysFont("Arial", 30)

    texto_score = fuente.render("SCORE", True, colores.WHITE)
    texto_score = pygame.transform.scale(texto_score, (75, 30))

    texto_puntuacion = fuente.render(str(puntuacion),True,colores.RED2)
    #texto_puntuacion = pygame.transform.scale(texto_puntuacion, (20, 40))

    screen.blit(texto_score, (50,10))
    screen.blit(texto_puntuacion, (50, 45))