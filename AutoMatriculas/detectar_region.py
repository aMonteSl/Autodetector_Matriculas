# detectar_region.py
from PIL import Image
import numpy as np
import math

def detectar_letra(matriz_pixeles):
    # Convertir la matriz de píxeles a una imagen PIL
    img = Image.fromarray(matriz_pixeles)

    # Obtener el ancho y el alto de la imagen
    ancho, alto = img.size

    # Crear un diccionario vacío para almacenar la frecuencia de los colores
    frecuencia = {}

    # Recorrer cada píxel de la imagen
    for x in range(ancho):
        for y in range(alto):
            # Obtener el color del píxel
            color = img.getpixel((x, y))
            # Si el color ya está en el diccionario, aumentar su frecuencia en uno
            if color in frecuencia:
                frecuencia[color] += 1
            # Si no, agregar el color al diccionario con frecuencia uno
            else:
                frecuencia[color] = 1

    # Ordenar el diccionario por frecuencia de mayor a menor
    frecuencia_ordenada = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)

    # El primer elemento del diccionario ordenado es el color más frecuente, que corresponde al fondo azul
    color_fondo = frecuencia_ordenada[0][0]

    # El segundo elemento del diccionario ordenado es el color menos frecuente, que corresponde a la letra blanca
    color_letra = frecuencia_ordenada[1][0]

    # Crear una lista vacía para almacenar las coordenadas de los píxeles que forman la letra
    coordenadas = []

    # Recorrer cada píxel de la imagen de nuevo
    for x in range(ancho):
        for y in range(alto):
            # Obtener el color del píxel
            color = img.getpixel((x, y))
            # Si el color es igual al color de la letra, agregar las coordenadas del píxel a la lista
            if color == color_letra:
                coordenadas.append((x, y))

    # Calcular el centro de masa de la letra, que es el promedio de las coordenadas de los píxeles que la forman
    x_centro = sum(x for x, y in coordenadas) / len(coordenadas)
    y_centro = sum(y for x, y in coordenadas) / len(coordenadas)

    # Crear un diccionario que asocia cada letra del alfabeto con su ángulo respecto al eje horizontal, en radianes
    angulos = {
        "A": 0,
        "B": 0.7853981633974483,
        "C": 1.5707963267948966,
        "D": 2.356194490192345,
        "E": 3.141592653589793,
        "F": -2.356194490192345,
        "G": -1.5707963267948966,
        "H": -0.7853981633974483,
        "I": 0,
        "J": 0.7853981633974483,
        "K": 1.5707963267948966,
        "L": 2.356194490192345,
        "M": 3.141592653589793,
        "N": -2.356194490192345,
        "O": -1.5707963267948966,
        "P": -0.7853981633974483,
        "Q": 0,
        "R": 0.7853981633974483,
        "S": 1.5707963267948966,
        "T": 2.356194490192345,
        "U": 3.141592653589793,
        "V": -2.356194490192345,
        "W": -1.5707963267948966,
        "X": -0.7853981633974483,
        "Y": 0,
        "Z": 0.7853981633974483
}

    # Crear una variable para almacenar la letra detectada
    letra_detectada = None

    # Crear una variable para almacenar la menor diferencia de ángulos entre la letra detectada y la letra real
    menor_diferencia = None

    # Recorrer cada letra del diccionario de ángulos
    for letra, angulo in angulos.items():
        # Calcular la diferencia de ángulos entre la letra y el centro de masa de la imagen
        diferencia = abs(angulo - math.atan2(y_centro, x_centro))
        # Si la diferencia es menor que la menor diferencia actual, o si la menor diferencia actual es None, actualizar la letra detectada y la menor diferencia
        if menor_diferencia is None or diferencia < menor_diferencia:
            letra_detectada = letra
            menor_diferencia = diferencia

    return letra_detectada
