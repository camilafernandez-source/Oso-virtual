from PIL import Image
from collections import deque
from pathlib import Path

carpeta = Path("assets/osito")

expresiones = [
    "normal",
    "feliz",
    "enojado",
    "triste",
    "confundido",
    "dormido"
]

def quitar_fondo(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada).convert("RGBA")

    ancho, alto = imagen.size
    pixeles = imagen.load()

    pendientes = deque()
    visitados = set()

    for x in range(ancho):
        pendientes.append((x, 0))
        pendientes.append((x, alto - 1))

    for y in range(alto):
        pendientes.append((0, y))
        pendientes.append((ancho - 1, y))

    while pendientes:
        x, y = pendientes.popleft()

        if (x, y) in visitados:
            continue

        visitados.add((x, y))

        r, g, b, a = pixeles[x, y]

        if r >= 245 and g >= 245 and b >= 245:
            pixeles[x, y] = (r, g, b, 0)

            for nx, ny in [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]:
                if 0 <= nx < ancho and 0 <= ny < alto:
                    pendientes.append((nx, ny))

    imagen.save(ruta_salida)

for expresion in expresiones:
    entrada = carpeta / f"osito_{expresion}.jpeg"
    salida = carpeta / f"osito_{expresion}_transparente.png"

    if entrada.exists():
        quitar_fondo(entrada, salida)
        print(f"¡{expresion} convertido!")
    else:
        print(f"No encontré: {entrada}")