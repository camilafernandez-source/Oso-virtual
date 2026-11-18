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
energia = 5
descenso = pygame.time.get_ticks()
fuente = pygame.font.Font(None, 40)

while ejecutando:
    #obtiene los eventos que ocurren en la ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            if (x - 400)**2 + (y - 300)**2 <= 100**2:
                estado_osito = "molesto"
                tiempo_enojo = pygame.time.get_ticks()
                print("Osh >:/")
    if estado_osito == "molesto":
        if pygame.time.get_ticks() - tiempo_enojo >= 2000:
            estado_osito = "normal"

    if pygame.time.get_ticks() - descenso >= 1000 and energia > 0:
        energia = energia - 1
        descenso = pygame.time.get_ticks()

    #pinta el fondo de un color
    ventana.fill((249, 245, 236))

    if energia == 0:
        estado_osito = "dormido"
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
    #barra
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

    #actualiza la pantalla
    pygame.display.flip()
pygame.quit()
