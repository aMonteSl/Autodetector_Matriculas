import cv2
import numpy as np
import os
import shutil

AREA_MIN = 100
VARIACION_MAXIMA = 400

class SegmentatorChars:
    def __init__(self, imagen_original):
        # Convertir la imagen a escala de grises si es una imagen a color
        if len(imagen_original.shape) > 2:
            self.imagen_original = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2GRAY)
        else:
            self.imagen_original = imagen_original

        self.imagen_binarizada = None

    def binarizar_con_otsu(self):
        # Aplicar el umbral de Otsu
        _, self.imagen_binarizada = cv2.threshold(self.imagen_original, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Invertir la imagen binarizada
        self.imagen_binarizada = cv2.bitwise_not(self.imagen_binarizada)

    def aplicar_apertura_cierre(self):
        # Definir un elemento estructurante 3x3
        elemento_estructurante = np.ones((3, 3), np.uint8)

        # Apertura
        imagen_apertura = cv2.morphologyEx(self.imagen_binarizada, cv2.MORPH_OPEN, elemento_estructurante)

        # Cierre
        imagen_cierre = cv2.morphologyEx(imagen_apertura, cv2.MORPH_CLOSE, elemento_estructurante)

        # Actualizar la imagen binarizada después de la apertura y el cierre
        self.imagen_binarizada = imagen_cierre

    def segmentar_caracteres(self):
        # Etiquetar las regiones conectadas
        _, etiquetas, stats, _ = cv2.connectedComponentsWithStats(self.imagen_binarizada)

        # Calcular la media de todas las áreas
        areas = stats[1:, cv2.CC_STAT_AREA]
        media_areas = np.mean(areas)

        # Crear una imagen en color para visualización
        imagen_coloreada = cv2.cvtColor(self.imagen_binarizada, cv2.COLOR_GRAY2BGR)

        # Lista para almacenar las BoundingBoxes
        bounding_boxes = []

        # Asignar un color aleatorio a cada región etiquetada (filtrando por área mínima y variación)
        for i in range(1, etiquetas.max() + 1):
            area = stats[i, cv2.CC_STAT_AREA]
            if AREA_MIN <= area  and ((media_areas - VARIACION_MAXIMA) <= area <= (media_areas + VARIACION_MAXIMA)):
                # Obtener las coordenadas de la BoundingBox
                x, y, width, height = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]

                # Dibujar la BoundingBox en la imagen
                cv2.rectangle(imagen_coloreada, (x, y), (x + width, y + height), (0, 255, 0), 2)

                # Almacenar la BoundingBox en la lista
                bounding_boxes.append((x, y, width, height))

        # Mostrar la imagen segmentada con las BoundingBoxes
        cv2.imshow('Segmentación de Caracteres', imagen_coloreada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Devolver la lista de BoundingBoxes
        return bounding_boxes

    def guardar_caracteres(self, bounding_boxes):
        # Ordenar las BoundingBoxes por la coordenada x
        bounding_boxes_ordenadas = sorted(bounding_boxes, key=lambda bbox: bbox[0])

        # Directorio donde se guardarán los caracteres
        directorio_caracteres = './Caracteres/Caracteres_Detectados/'

        # Crear el directorio si no existe
        os.makedirs(directorio_caracteres, exist_ok=True)

        # Eliminar el contenido del directorio
        for archivo in os.listdir(directorio_caracteres):
            archivo_path = os.path.join(directorio_caracteres, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)

        # Guardar cada carácter en una imagen por separado en el directorio específico
        for i, bbox in enumerate(bounding_boxes_ordenadas):
            x, y, width, height = bbox
            caracter_recortado = self.imagen_original[y:y+height, x:x+width]

            # Guardar el carácter recortado en el directorio específico
            cv2.imwrite(os.path.join(directorio_caracteres, f'caracter_{i+1}.png'), caracter_recortado)


    def mostrar_resultados(self):
        # Mostrar la imagen original y la binarizada después de la apertura y el cierre
        cv2.imshow('Imagen Binarizada con Apertura y Cierre', self.imagen_binarizada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def start(self):
        self.binarizar_con_otsu()
        self.aplicar_apertura_cierre()
        bounding_boxes = self.segmentar_caracteres()
        self.guardar_caracteres(bounding_boxes)
        print('Tras la segmentación de cada caracter, hemos etiquetado {} objetos en la imagen (pueden existir objetos etiquetados erroneamente)'.format(len(bounding_boxes)))


