import pygame
import colores
import random
from ui import *
from Nave import *
from funciones_generales import *
import sqlite3

with sqlite3.connect("bd_btf.db") as conexion:

    try:
        sentencia = ''' create table jugador   
                    (
                    id integer primary key autoincrement,
                    nombre text,
                    score text
                    )                       
                '''

        conexion.execute(sentencia)
        print("se creo tabla jugador.")
    except sqlite3.OperationalError:
        print("La tabla personajes ya existe")


    #~~~~~~~~~~~~~~~~~~~~~CONSTANTES Y VARIABLES~~~~~~~~~~~~~~~~~~~~
    ANCHO_PANTALLA = 1100
    ALTO_PANTALLA = 900
    FPS = 60
    fondo_estrellas = "imagenes/fondo.jpg"
    img_inicio = "imagenes/Pantalla inicio.png"
    img_nave = "imagenes/nave.png"
    img_ufo = "imagenes/enemigos.png"
    img_disparo = "imagenes/disparo.png"
    posicion_inicio = [450,800]

    disparos = []
    contador_tandas = 0

    #~~~~~~~~~~~~~~~~~~~~~INICIO PYGAME Y COSAS INDISPENSABLES~~~~~~~~~~~~~~~~~~~~~~
    pygame.init()
    screen = pygame.display.set_mode((ANCHO_PANTALLA ,ALTO_PANTALLA))
    pygame.display.set_caption("GALAXY UTN")

    #~~~~~~~~~~~OBJETOS~~~~~~~~~~~~~~~~~~~~~~
    jugador = Nave(img_nave,posicion_inicio,60,60)
    enemigos = []
    rectangulos_enemigos = []

    #~~~~~~~~~~IMAGENES~~~~~~~~~~~~~~~~~~~
    fondo_inicio_partida = pygame.image.load(fondo_estrellas)
    fondo_inicio_partida = pygame.transform.scale(fondo_inicio_partida,(ANCHO_PANTALLA,ALTO_PANTALLA))


    #~~~~~~~~~~~~~~~~~~~~~FLAGS Y CONTADORES~~~~~~~~~~~~~~~~~~~~~~~
    run = True
    iniciar = True
    contador_segundos = 0
    flag_ida = True

    #~~~~~~~~~~~~~~TIMER~~~~~~~~~~~~~~~~~~
    timer = pygame.USEREVENT
    pygame.time.set_timer(timer,500)
    reloj = pygame.time.Clock()
    #~~~~~~~~~~~~~~INICIO DE JUEGO~~~~~~~~~~~~~~
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.USEREVENT:
                contador_segundos += 1
                print(contador_segundos)

            if event.type == pygame.KEYDOWN:#~~~~~~~~~~~~~~~~~~~~~~~~~~DETECTA BOTON DE DISPARO Y DISPARA SI SE CUMPLE LA CONDICION~~~~~~~~~~~~~~~~~~~~~
                if event.key == pygame.K_z and len(disparos) < jugador.cant_disparos:
                    disparos.append(crear_disparo(img_disparo,jugador.posicion.copy()))


        if iniciar == True: #~~~DENTRO DE LA PARTIDA~~
            screen.blit(fondo_inicio_partida, (0, 0))
            screen.blit(jugador.imagen,(jugador.posicion))

            mostrar_puntuacion(jugador.puntos,screen)

            if len(enemigos) == 0:

                contador_tandas += 1
                if len(disparos) > 0:
                    disparos.clear()


                generar_tandas(enemigos, rectangulos_enemigos, img_ufo, contador_tandas)
            for enemigo in enemigos:#COMPORTAMIENTO DE LOS ENEMIGOS
                enemigo.moverse(1,1,0,ANCHO_PANTALLA)
                screen.blit(enemigo.imagen,(enemigo.posicion))

            lista_teclas = pygame.key.get_pressed()

            if True in lista_teclas:
                jugador.mover_nave(ANCHO_PANTALLA,lista_teclas)

            for disparo in disparos:#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TODO RELACIONADO CON disparos~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                pos = 0

                screen.blit(disparo.imagen,(disparo.posicion))
                disparo.posicion[1] -= (5)

                if disparo.posicion[1] < 0 :
                    disparos.remove(disparo)

                disparo.update_posicion()
                flag_del = 0
                aux_del = 0

                for en in range(len(enemigos)):

                    if detectar_colicion(disparo.rect, enemigos[en].rect):
                        aux_del = en
                        flag_del = 1
                        print(aux_del)
                        disparos.remove(disparo)
                        jugador.sumar_punto(100)

                if flag_del:
                    enemigos[aux_del].morir()
                    rectangulos_enemigos.pop(aux_del)
                    del enemigos[aux_del]

                    flag_del = 0

        reloj.tick(FPS)
        pygame.display.flip()