import pygame
from pathlib import Path

#inicia pygame
pygame.init()
#modulo que usaremos
ANCHO=800
ALTO=600

#dimensiones de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
#superficie de la ventana con el titulo
pygame.display.set_caption("Mi osito virtual")

#cargar imagenes
RUTA_ASSETS = Path(__file__).resolve().parent / "assets"
fondo_habitacion = pygame.image.load(
    RUTA_ASSETS / "habitacion" / "fondo_habitacion.png"
).convert() #adapta la imagen para pygame

ventana_dia = pygame.image.load(
    RUTA_ASSETS / "habitacion" / "ventana_dia.png"
).convert_alpha()

ventana_noche = pygame.image.load(
    RUTA_ASSETS / "habitacion" / "ventana_noche.png"
).convert_alpha() #para conservar transparencia

expresiones_osito = {
    "normal": pygame.image.load(
        RUTA_ASSETS / "osito" / "osito_normal_transparente.png"
    ).convert_alpha(),

    "molesto": pygame.image.load(
        RUTA_ASSETS / "osito" / "osito_enojado_transparente.png"
    ).convert_alpha(),

    "dormido": pygame.image.load(
            RUTA_ASSETS / "osito" / "osito_dormido_transparente.png"
        ).convert_alpha(),
}
menu_acciones = pygame.image.load(
    RUTA_ASSETS / "interfaz" / "menu_acciones.png"
).convert_alpha()
globo_dialogo = pygame.image.load(
    RUTA_ASSETS / "interfaz" / "globo_dialogo.png"
).convert_alpha()


#recorre el diccionario de expresiones
for estado, imagen in expresiones_osito.items():
    expresiones_osito[estado] = pygame.transform.smoothscale(
        imagen, (548, 548)
    )

#distingue los pixeles visibles de los transparentes
POS_OSITO = (298, 115)
POS_MENU = (21, 459)
POS_GLOBO = (219, 115)

boton_comida = pygame.Rect(37, 471, 68, 68)
boton_jugar = pygame.Rect(130, 471, 68, 68)
boton_accesorios = pygame.Rect(223, 471, 68, 68)
boton_dormir = pygame.Rect(316, 471, 68, 68)
boton_bloqueado = pygame.Surface((68,68), pygame.SRCALPHA)

pygame.draw.rect(
    boton_bloqueado, 
    (80, 59, 70, 120),
    (0,0,68,68),
    border_radius=16
)

mascaras_osito={}
for estado, imagen in expresiones_osito.items():
    mascaras_osito[estado] = pygame.mask.from_surface(imagen)
ejecutando = True

#barras de necesidades
ANCHO_BARRA = 312
ALTO_BARRA = 16

COLOR_FONDO_BARRA = "#DFD5C6"
COLOR_ENERGIA = "#EABF7F"
COLOR_HAMBRE = "#A4CBA7"
COLOR_FELICIDAD = "#DDA8BB"
COLOR_TEXTO = "#503B46"

estado_osito = "normal"
tiempo_enojo = 0

energia = 100
descenso_sueño = pygame.time.get_ticks()

hambre = 25
descenso_hambre = pygame.time.get_ticks()

felicidad = 70
descenso_felicidad = pygame.time.get_ticks()
caricia = pygame.time.get_ticks()
inicio_click = None
acariciando = False

fuente_dialogo = pygame.font.Font(
    RUTA_ASSETS / "fuentes" / "Nunito-Regular.ttf",
    18
)
fuente_barras = pygame.font.Font(
    RUTA_ASSETS / "fuentes" / "Nunito-Regular.ttf",
    14
)

def dibujar_barra (x,y, valor, color, etiqueta):
    #texto
    texto = fuente_barras.render(
        etiqueta, True, COLOR_TEXTO
    )
    rect_texto = texto.get_rect(
        topright=(x + ANCHO_BARRA, y)
    )

    ventana.blit(texto, rect_texto)
    #posicion vertical
    y_barra= y + 18
    pygame.draw.rect(
        ventana,
        COLOR_FONDO_BARRA,
        (x,y_barra,ANCHO_BARRA,ALTO_BARRA),
        border_radius=8
    )
    #calcula el ancho del relleno
    ancho_actual = int(ANCHO_BARRA*valor/100)
    if ancho_actual >0:
        pygame.draw.rect(
            ventana,
            color,
            (x,y_barra,ancho_actual,ALTO_BARRA),
            border_radius=8
        )
#funciones que comprieba si estamos tocando un pixel visible
def tocar_osito(x,y):
    local_x = x - POS_OSITO[0]
    local_y = y - POS_OSITO[1]

    if 0 <= local_x < 548 and 0 <= local_y < 548:
        return mascaras_osito[estado_osito].get_at(
            (local_x, local_y)
        )
    return False

def obtener_mensaje():
    if estado_osito == "dormido":
        return "Zzz.."
    elif estado_osito == "molesto":
        return "Ush"
    elif hambre <30:
        return "Tengo hambre :("
    elif energia <30:
        return "Tengo sueñooo.."
    elif felicidad < 30:
        return "Me siento solo.."
    else:
        return "Holaa"

while ejecutando:
    #obtiene los eventos que ocurren en la ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                x, y = evento.pos

                if boton_comida.collidepoint(evento.pos):
                    if hambre < 100 and estado_osito != "dormido":
                        hambre = min(100, hambre + 20)
                #evita que un mismo click active el boton e interactue con el oso
                elif tocar_osito(x,y):
                    inicio_click = evento.pos
                    acariciando = False
                

        if evento.type == pygame.MOUSEMOTION:
            x,y = evento.pos

            if inicio_click is not None:
                if (x - inicio_click[0])**2 + (y - inicio_click[1])**2 > 10**2:
                    acariciando = True
            #comprueba si estamos manteniendo el boton presionado
            if acariciando and evento.buttons[0]:
                if tocar_osito(x,y):
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

    if energia == 0:
        estado_osito = "dormido"
    elif energia >= 100 and estado_osito == "dormido":
        energia = 100
        estado_osito = "normal"
        
    #blit dibuja una imagen sobre otra
    ventana.blit(fondo_habitacion, (0,0))
    if estado_osito == "dormido":
        ventana.blit(ventana_noche, (60, 72))
    else:
        ventana.blit(ventana_dia, (60, 72))

    #dibuja al osito segun el estado
    ventana.blit(expresiones_osito[estado_osito], POS_OSITO)
    ventana.blit(menu_acciones, POS_MENU)

    #modifica la apariencia del bloque
    if hambre == 100 or estado_osito == "dormido":
        ventana.blit(boton_bloqueado, boton_comida.topleft)
    ventana.blit(globo_dialogo, POS_GLOBO)

    #selecciona el mensaje segun el estado del osito
    mensaje = obtener_mensaje()
    texto_dialogo = fuente_dialogo.render(
        mensaje, True, (80, 59, 70)
    )
    rect_texto = texto_dialogo.get_rect(
        center=(329, 157)
    )
    ventana.blit(texto_dialogo,rect_texto)

    dibujar_barra(471,11, energia, COLOR_ENERGIA, "Energía")
    dibujar_barra(471,57,hambre, COLOR_HAMBRE, "Hambre")
    dibujar_barra(471,103,felicidad,COLOR_FELICIDAD, "Felicidad")
    #actualiza la pantalla
    pygame.display.flip()

pygame.quit()
