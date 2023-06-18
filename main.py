import pygame
import colores
import random
from boton import Boton
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

    posicion_inicio = [450,800]

    disparos = []
    contador_tandas = 0

    #~~~~~~~~~~~~~~~~~~IMAGENES Y SONIDOS~~~~~~~~~~~~~~~~~
    fondo_estrellas = cargar_imagen("imagenes/fondo.jpg", [ANCHO_PANTALLA, ALTO_PANTALLA])
    img_inicio = cargar_imagen("imagenes/Pantalla inicio.png", [ANCHO_PANTALLA, ALTO_PANTALLA])
    img_nave = cargar_imagen("imagenes/nave.png", [60, 60])
    img_ufo = cargar_imagen("imagenes/enemigos.png", [50, 50])
    img_disparo = cargar_imagen("imagenes/disparo.png", [15, 15])
    img_boton = cargar_imagen("imagenes/botonJugar1.png", [200,200])
    img_boton2 = cargar_imagen("imagenes/BotonJugar1.png", [100,100])

    sonido_disparo = cargar_sonido("sonidos/Collision8-Bit.ogg",0.3)
    sonido_muerte = cargar_sonido("sonidos/EnemyDeath.ogg",0.2)
    sonido_levelup = cargar_sonido("sonidos/Powerup.ogg",0.4)

    #~~~~~~~~~~~~~~~~~~~~~INICIO PYGAME Y COSAS INDISPENSABLES~~~~~~~~~~~~~~~~~~~~~~
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((ANCHO_PANTALLA ,ALTO_PANTALLA))
    pygame.display.set_caption("GALAXY UTN")

    #~~~~~~~~~~~OBJETOS~~~~~~~~~~~~~~~~~~~~~~
    jugador = Nave(img_nave,posicion_inicio,60,60)
    enemigos = []
    rectangulos_enemigos = []
    boton_jugar = Boton(450,350,img_boton,img_boton2)

    #~~~~~~~~~~~~~~~~~~~~~FLAGS Y CONTADORES~~~~~~~~~~~~~~~~~~~~~~~
    run = True
    iniciar = False
    contador_segundos = 0
    flag_ida = True
    flag_nombre = True
    flag_x = 0


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
                if event.key == pygame.K_z and len(disparos) < jugador.cant_disparos and iniciar:
                    sonido_disparo.play()
                    disparos.append(crear_disparo(img_disparo,jugador.posicion.copy()))

            if event.type == pygame.MOUSEBUTTONDOWN:#DETECTA CLICK DEL MOUSE
                if boton_jugar.rect.collidepoint(pygame.mouse.get_pos()) and iniciar == False:
                    iniciar = True


        if iniciar == True: #~~~DENTRO DE LA PARTIDA~~
            screen.blit(fondo_estrellas, (0, 0))
            screen.blit(jugador.imagen,(jugador.posicion))

            mostrar_puntuacion(jugador.puntos,screen)

            if len(enemigos) == 0:

                generar_tandas(enemigos, rectangulos_enemigos, img_ufo, contador_tandas)
                sonido_levelup.play()

                if len(disparos) > 0:
                    disparos.clear()

                contador_tandas += 1

            for enemigo in enemigos:#COMPORTAMIENTO DE LOS ENEMIGOS

                if contador_tandas > 0:
                    if flag_x <= 75:
                        enemigo.mover_enemigo(1)

                    elif flag_x <= 150:
                        enemigo.mover_enemigo(-1)

                        if flag_x == 150:
                            flag_x = 0

                    enemigo.rect.topleft = enemigo.posicion
                    rectangulos_enemigos.append(enemigo.rect)

                screen.blit(enemigo.imagen, (enemigo.posicion))


            flag_x += 1


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
                        sonido_muerte.play()
                        jugador.sumar_punto(100)

                if flag_del:
                    enemigos[aux_del].morir()
                    rectangulos_enemigos.pop(aux_del)
                    del enemigos[aux_del]

                    flag_del = 0
        else:#PANTALLA DE INICIO DEL JUEGO
            screen.blit(img_inicio,(0,0))
            if flag_nombre:
                screen.blit(boton_jugar.imagen1, (boton_jugar.rect.x, boton_jugar.rect.y))


        reloj.tick(FPS)
        pygame.display.flip()