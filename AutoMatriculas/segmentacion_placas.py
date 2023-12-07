import cv2
import numpy as np

class PlacaRegionProcessor:
    def __init__(self):
        # Parámetros configurables
        self.PREPROCESAMIENTO_MEDIAN_BLUR = 5
        self.PREPROCESAMIENTO_BINARIZACION = 150
        self.PREPROCESAMIENTO_DILATACION_ITER = 2
        self.PREPROCESAMIENTO_EROSION_ITER = 1

    def preprocesar_placa_region(self, placa_region):
        # Aplicar mediana para reducir el ruido
        placa_region_suavizada = cv2.medianBlur(placa_region, self.PREPROCESAMIENTO_MEDIAN_BLUR)

        # Convertir a escala de grises
        placa_region_gris = cv2.cvtColor(placa_region_suavizada, cv2.COLOR_BGR2GRAY)

        # Aplicar umbral para obtener el rectángulo azul
        _, placa_nation_bin = cv2.threshold(placa_region_gris, 100, 255, cv2.THRESH_BINARY_INV)

        # Encontrar contornos y obtener el rectángulo azul
        contornos, _ = cv2.findContours(placa_nation_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contornos:
            x, y, w, h = cv2.boundingRect(max(contornos, key=cv2.contourArea))
            placa_nation = placa_region[y:y+h, x:x+w]
        else:
            placa_nation = np.zeros_like(placa_region)

        # Aplicar dilatación y erosión para mejorar la forma del rectángulo azul
        placa_nation_bin = cv2.dilate(placa_nation_bin, None, iterations=self.PREPROCESAMIENTO_DILATACION_ITER)
        placa_nation_bin = cv2.erode(placa_nation_bin, None, iterations=self.PREPROCESAMIENTO_EROSION_ITER)

        return placa_nation

    def procesar_placa_region(self, placa_region_path):
        placa_region = cv2.imread(placa_region_path)
        if placa_region is None:
            print(f'Error: No se puede leer la imagen {placa_region_path}.')
            return None

        placa_nation = self.preprocesar_placa_region(placa_region)

        # Guardar la imagen generada
        cv2.imwrite("placa_nation.jpg", placa_nation)

        return placa_nation

