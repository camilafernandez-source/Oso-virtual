import pygame

#inicia pygame
pygame.init()
#modulo que usaremos
ANCHO=800
ALTO=600

#dimensiones de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
#superficie de la ventana con el titulo
pygame.display.set_caption("Mi osito virtual")

ejecutando = True

estado_osito = "normal"
tiempo_enojo = 0

energia = 100
descenso_sueño = pygame.time.get_ticks()

hambre = 25
descenso_hambre = pygame.time.get_ticks()

fresa_disponible = True
tiempo_comida = 0

felicidad = 70
descenso_felicidad = pygame.time.get_ticks()
caricia = pygame.time.get_ticks()
inicio_click = None
acariciando = False

fuente = pygame.font.Font(None, 40)

while ejecutando:
    #obtiene los eventos que ocurren en la ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                x, y = evento.pos

                if (x - 400)**2 + (y - 300)**2 <= 100**2:
                    inicio_click = evento.pos
                    acariciando = False

            if fresa_disponible and 600 <= x <= 650 and 350 <= y <= 410:
                hambre = min(100, hambre + 20)
                fresa_disponible = False
                tiempo_comida = pygame.time.get_ticks()
                print("🍓")

        if evento.type == pygame.MOUSEMOTION:
            x,y = evento.pos

            if inicio_click is not None:
                if (x - inicio_click[0])**2 + (y - inicio_click[1])**2 > 10**2:
                    acariciando = True
            #comprueba si estamos manteniendo el boton presionado
            if acariciando and evento.buttons[0]:
                if (x - 400)**2 + (y - 300)**2 <= 110**2:

                    if pygame.time.get_ticks() - caricia >= 500:
                        felicidad = min(100, felicidad + 1)
                        caricia = pygame.time.get_ticks()
        if evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and inicio_click is not None:

                if not acariciando:
                    if estado_osito == "dormido":
                        if energia < 50:
                            estado_osito = "molesto"
                            tiempo_enojo = pygame.time.get_ticks()
                    else:
                        estado_osito = "molesto"
                        tiempo_enojo = pygame.time.get_ticks()
                inicio_click = None
                acariciando = False
    if not fresa_disponible:
        if pygame.time.get_ticks() - tiempo_comida >= 5000:
            fresa_disponible = True

    if estado_osito == "molesto":
        if pygame.time.get_ticks() - tiempo_enojo >= 2000:
            estado_osito = "normal"

    if pygame.time.get_ticks() - descenso_sueño >= 1000:
        if estado_osito == "dormido":
            energia = energia + 1
        elif energia > 0:
            energia = energia - 1
        descenso_sueño = pygame.time.get_ticks()

    if pygame.time.get_ticks() - descenso_hambre >= 3000:
        if hambre > 0:
            hambre = hambre - 1
        descenso_hambre = pygame.time.get_ticks()

    if pygame.time.get_ticks() - descenso_felicidad >=5000:
        if felicidad > 0 and not acariciando:
            felicidad = felicidad - 1
        descenso_felicidad = pygame.time.get_ticks()

    #pinta el fondo de un color
    ventana.fill((249, 245, 236))

    if energia == 0:
        estado_osito = "dormido"
    elif energia >= 100 and estado_osito == "dormido":
        energia = 100
        estado_osito = "normal"

    #orejitas
        #derecha
    pygame.draw.circle(
        ventana,
        (181,133,99),
        (480, 240),
        50
    )
    
        #izq
    pygame.draw.circle(
        ventana,
        (181,133,99),
        (320, 240),
        50
    )
    
    #dibuja circulo provisional
    pygame.draw.circle(
        ventana,
        (181,133,99), #color
        (400,300), #centro
        110 #radio
    )

    if estado_osito == "normal":
    #ojitos
        #izq
        pygame.draw.circle(
            ventana,
            (80,59,70),
            (365, 285),
            15
        )
        #derecho
        pygame.draw.circle(
            ventana,
            (80,59,70),
            (435, 285),
            15
        )
    elif estado_osito == "molesto" :
        pygame.draw.line(
            ventana,
            (80,59,70),
            (350,280),
            (380,290),
            7
        )
        pygame.draw.line(
            ventana,
            (80,59,70),
            (420,290),
            (450,280),
            7
        )
    elif estado_osito == "dormido":
        pygame.draw.line(
            ventana,
            (80,59,70),
            (350,285),
            (380,285),
            7
        )
        pygame.draw.line(
            ventana,
            (80,59,70),
            (420,285),
            (450,285),
            7
        )

    #hocico
    pygame.draw.ellipse(
        ventana,
        (235, 193, 167),
        (373, 310, 55, 65)
    )

    # Naricita
    pygame.draw.polygon(
        ventana,
        (80, 59, 70),
        [(390, 330), (410, 330), (400, 340)]
    )

    # Boquita de molesto
    if estado_osito == "molesto":
        pygame.draw.lines(
            ventana,
            (80, 59, 70),
            False,
            [(390, 360), (400, 350), (410, 360)],
            5
        )

    if estado_osito == "dormido":
        #render convierte el texto en una superficie
        texto = fuente.render("Zzz", True, (80, 59, 70))
        #blit coloca esa superficie en la ventana con las coordenadas
        ventana.blit(texto, (510, 180))
    #barra sueño
    pygame.draw.rect(
        ventana,
        (233,201,210),
        (50,50,200,25)
    )
    #energia actual
    pygame.draw.rect(
        ventana,
        (182,142,156),
        (50,50, energia*2,25)
    )

    if hambre < 30:
        #crea el texto de hambre
        texto_hambre = fuente.render(
            "tengo hambre :(",
            True,
            (80,59,70)
        )
        ventana.blit(texto_hambre,(300,450))

    #barra saciedad
    pygame.draw.rect(
        ventana,
        (233,201,210),
        (50, 90, 200, 25)
    )
        #hambre actual
    pygame.draw.rect(
        ventana,
        (182, 142, 156),
        (50, 90, hambre * 2, 25)
    )
    
    if fresa_disponible:
        #fresa
        pygame.draw.ellipse(
            ventana,
            (229,11,121),
            (600,350,50,60)
        )
        pygame.draw.polygon(
            ventana,
            (108,155,112),
            [(600,355), (610,340),(625,350),
            (640,340), (650,355),(625,360)]
        )

    #barra cariño
    pygame.draw.rect(
        ventana,
        (233, 201, 210),
        (50, 130, 200, 25)
    )

    pygame.draw.rect(
        ventana,
        (182, 142, 156),
        (50, 130, felicidad * 2, 25)
    )

    #actualiza la pantalla
    pygame.display.flip()
pygame.quit()
