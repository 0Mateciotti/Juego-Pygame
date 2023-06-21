import pygame
import colores
from boton import Boton
from ui import *
from Nave import *
from funciones_generales import *
import sqlite3
import random

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

    lista_jugadores = conexion.execute("SELECT * FROM jugador")

    #~~~~~~~~~~~~~~~LISTAS~~~~~~~~~~~~
    enemigos = []
    rectangulos_enemigos = []
    lista_puntajes = []
    disparos = []
    disparos_enemigos = []
    #~~~~~~~~~~~~~~~~~~IMAGENES~~~~~~~~~~~~~~~~~
    fondo_estrellas = cargar_imagen("imagenes/fondo.jpg", [ANCHO_PANTALLA, ALTO_PANTALLA])

    img_inicio = cargar_imagen("imagenes/Pantalla inicio.png", [ANCHO_PANTALLA, ALTO_PANTALLA])

    img_nave = cargar_imagen("imagenes/nave.png", [60, 60])

    img_ufo = cargar_imagen("imagenes/enemigos.png", [50, 50])

    img_disparo = cargar_imagen("imagenes/disparo.png", [15, 15])

    img_boton = cargar_imagen("imagenes/botonJugar1.png", [200,200])
    img_boton2 = cargar_imagen("imagenes/BotonJugar1.png", [100,100])
    #~~~~~~~~~~~~~~~SONIDOS~~~~~~~~~~~~~~~
    sonido_disparo = cargar_sonido("sonidos/Collision8-Bit.ogg",0.3)
    sonido_muerte = cargar_sonido("sonidos/EnemyDeath.ogg",0.2)
    sonido_levelup = cargar_sonido("sonidos/Powerup.ogg",0.4)
    #~~~~~~~~~~~~~~~~~~~~~INICIO PYGAME Y COSAS INDISPENSABLES~~~~~~~~~~~~~~~~~~~~~~
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((ANCHO_PANTALLA ,ALTO_PANTALLA))
    pygame.display.set_caption("GALAXY UTN")
    fuente = pygame.font.SysFont("Arial", 30)
    img_puntajes = fuente.render("PUNTAJES", True, colores.WHITE)
    #~~~~~~~~~~~OBJETOS~~~~~~~~~~~~~~~~~~~~~~
    jugador = Nave(img_nave,posicion_inicio,60,60)

    boton_jugar = Boton(450,350,img_boton)

    boton_puntajes = Boton(460,520,img_puntajes)
    #~~~~~~~~~~~~~~~~~~~~~FLAGS~~~~~~~~~~~~~~~~~~~~~~~
    run = True
    iniciar = False
    flag_ida = True
    flag_nombre = False
    flag_x = False
    flag_lista_jugadores = True
    flag_morir = False
    flag_jugador = True
    #~~~~~~~~~~~CONTADORES/OTROS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    contador_segundos = 0
    contador_lista_jugadores = 0
    contador_tandas = 0
    nombre_jugador = ""
    img_nombre_jugador = ""
    #~~~~~~~~~~~~~~TIMER~~~~~~~~~~~~~~~~~~
    timer = pygame.USEREVENT
    pygame.time.set_timer(timer,500)
    reloj = pygame.time.Clock()
    #~~~~~~~~~~~~~~INICIO DE JUEGO~~~~~~~~~~~~~~
    while run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:#DETECTA SI CERRAMOS EL JUEGI
                run = False

            if flag_morir:#~~~~~~~~~~~~~~~~~~~~~DETECTO CUANDO MUERE Y CREA EL PERFIL DEL JUGADOR Y RESETEO VALORES PARA VOLVER A INICIAR~~~~~~~~~~~~~~~~~~~~
                try:
                    conexion.execute("insert into jugador(nombre,score) values (?,?)",(nombre_jugador,jugador.puntos))
                    conexion.commit()
                    print("Jugador cargado")
                except:
                    print("Erorr")


                pygame.quit()

            if event.type == pygame.USEREVENT:#TIMER SEGUNDOS
                contador_segundos += 1
                print(contador_segundos)

            if event.type == pygame.KEYDOWN:#~~~~~~~~~~~~~~~~~~~~~~~~~~DETECTA BOTON DE DISPARO Y DISPARA SI SE CUMPLE LA CONDICION~~~~~~~~~~~~~~~~~~~~~

                if event.key == pygame.K_z and len(disparos) < jugador.cant_disparos and iniciar:
                    sonido_disparo.play()
                    disparos.append(crear_disparo(img_disparo,jugador.posicion.copy()))

                if flag_nombre == False:#~~~~~~~~~~~~INGRESO DE NOMBRE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    if event.key == pygame.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[0:-1]

                    elif len(nombre_jugador) < 12 and event.key != pygame.K_RETURN:
                        nombre_jugador += event.unicode

                    if event.key == pygame.K_RETURN:
                        flag_nombre = True
                        print(f'Nombre final: "{nombre_jugador}"')

            if event.type == pygame.MOUSEBUTTONDOWN:#DETECTA CLICK DEL MOUSE

                if boton_jugar.rect.collidepoint(pygame.mouse.get_pos()) and iniciar == False and flag_nombre == True:
                    iniciar = True
                    contador_segundos = 0
                    print("AAAAAAAAAAAAAA")

        if iniciar == True: #~~~DENTRO DE LA PARTIDA~~

            screen.blit(fondo_estrellas, (0, 0))
            screen.blit(jugador.imagen,(jugador.posicion))

            mostrar_puntuacion(jugador.puntos,screen)

            if len(enemigos) == 0:#~~~~~~~~~~~~~~~~~~~DETECTA CUANDO MATAMOS A TODOS LOS ENEMIGOS~~~~~~~~~~~~~~~~~~~
                generar_tandas(enemigos, rectangulos_enemigos, img_ufo, contador_tandas)
                sonido_levelup.play()
                if contador_tandas > 0 and jugador.cant_disparos < 10:
                    jugador.cant_disparos += 1
                    jugador.velocidad += 0.1

                if len(disparos) > 0:
                    disparos.clear()

                contador_tandas += 1

            for enemigo in enemigos:#COMPORTAMIENTO DE LOS ENEMIGOS
                enemigo.rect.topleft = enemigo.posicion
                rectangulos_enemigos.append(enemigo.rect)

                movimiento = random.randint(1,2)
                if contador_tandas > 0:
                    if flag_x <= 75 and enemigo.posicion[0] < 1050:
                        enemigo.mover_enemigo(movimiento)

                    elif flag_x <= 150 and enemigo.posicion[0] > 0:
                        enemigo.mover_enemigo(-movimiento)

                        if flag_x == 150:
                            flag_x = 0

                screen.blit(enemigo.imagen, (enemigo.posicion))

            flag_x += 1

            lista_teclas = pygame.key.get_pressed()

            if True in lista_teclas:
                jugador.mover_nave(ANCHO_PANTALLA,lista_teclas)

            for disparo in disparos:#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TODO RELACIONADO CON DISPAROS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
                        try:
                            disparos.remove(disparo)
                        except:
                            print("el disparo ya no existe.")
                        pygame.mixer.stop()
                        sonido_muerte.play()
                        jugador.sumar_punto(100)

                if flag_del:
                    enemigos[aux_del].morir()
                    rectangulos_enemigos.pop(aux_del)
                    del enemigos[aux_del]

                    flag_del = 0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DISPAROS ENEMIGOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            if contador_segundos == 5 and flag_nombre and iniciar:
                contador_segundos = 0


                if len(enemigos) > 0:
                    for i in range(random.randint(0,len(enemigos))):

                        posicion_random = random.randint(0,len(enemigos)-1)

                        disparos_enemigos.append(crear_disparo(img_disparo,enemigos[posicion_random].posicion))

            for disparo_enemigo in disparos_enemigos:#~~~~~~~~~~~~~~~VALIDO COLICIONES Y MUEVO LOS DISPAROS~~~~~~~~~~~~~~~~~~~~~~~~~~
                disparo_enemigo.update_posicion()
                screen.blit(disparo_enemigo.imagen, disparo_enemigo.posicion)

                disparo_enemigo.posicion[1] += 5

                if disparo_enemigo.posicion[0] >= ALTO_PANTALLA:#~~~~~~~~~~~~~~~~~BORRO DISPARO DEL ENEMIGO SI SALE DE LA PANTALLA~~~~~~~~~~~~~~
                    disparos_enemigos.remove(disparo_enemigo)


                if disparo_enemigo.rect.colliderect(jugador.rect):
                    flag_morir = True
                    iniciar = False

        elif iniciar == False and flag_morir == False: #PANTALLA DE INICIO DEL JUEGO
            salto = 40
            screen.blit(img_inicio,(0,0))
            cursor = conexion.execute("SELECT * FROM jugador")

            if flag_jugador:#~~~~~~~SUBO LA DATA DEL JUGADOR A LA BASE DE DATOS~~~~~~~~~~~~~~~~~~~~~~~
                for fila in cursor:
                    aux = fuente.render(f"{fila[1]} {fila[2]}", True, colores.RED2)
                    lista_puntajes.append(aux)
                    flag_jugador = False

            for i in range(10 if len(lista_puntajes) > 10 else len(lista_puntajes)):#~~~~~~~MUESTRO LOS JUGADORES ANTERIORES EN PANTALLA~~~~~~~~~~~~~
                try:
                    print(i)
                    screen.blit(lista_puntajes[i], (60, 350 + salto))
                    salto += 40
                except:
                    print("a")
                contador_lista_jugadores += 1

            if flag_nombre:
                screen.blit(boton_jugar.imagen1, (boton_jugar.rect.x, boton_jugar.rect.y))#~~~~~~~~~~~UNA VEZ QUE INGRESA EL NOMBRE SALE EL BOTON DE JUGAR~~~~~~~~~~~~~~

            else:
                pygame.draw.rect(screen,(255,255,255),[420,430,230,75])
                pygame.draw.rect(screen,(0,0,0),[420,430,230,75],8)
                img_nombre_jugador = fuente.render(nombre_jugador, True, colores.BLACK)
                screen.blit(img_nombre_jugador, [440, 450])



        reloj.tick(FPS)
        pygame.display.flip()