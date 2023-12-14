import cv2

class PlacaDetector:
    def __init__(self):
        # Parámetros configurables
        self.SIGMA_X = 1
        self.AREA_CONTORNO_MINIMA_PLACA = 2000  # Ajustar el área mínima para la detección de la placa
        self.APROX_POLYDP_FACTOR = 0.02  # Reducir el factor de aproximación

    def preprocesar_imagen(self, imagen):
        # Aplicar ecualización del histograma para mejorar el contraste
        img_yuv = cv2.cvtColor(imagen, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        imagen = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        # Aplicar suavizado Gaussiano con sigmaX ajustable
        suavizado = cv2.GaussianBlur(imagen, (5, 5), sigmaX=self.SIGMA_X)
        
        return suavizado

    def identificar_placa(self, contornos):
        for cnt in contornos:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, self.APROX_POLYDP_FACTOR * cv2.arcLength(cnt, True), True)

            # Buscar un objeto rectangular blanco en la imagen
            if len(approx) == 4 and area > self.AREA_CONTORNO_MINIMA_PLACA:
                return cnt

        return None

    def detectar_placa(self, imagen_path):
        imagen = cv2.imread(imagen_path)
        if imagen is None:
            print(f'Error: No se puede leer la imagen {imagen_path}.')
            return None

        procesada = self.preprocesar_imagen(imagen)
        gris = cv2.cvtColor(procesada, cv2.COLOR_BGR2GRAY)

        # Aplicar el umbral de Otsu para segmentación
        _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        placa_contorno = self.identificar_placa(contornos)
        if placa_contorno is not None:
            x, y, w, h = cv2.boundingRect(placa_contorno)
            placa_region = imagen[y:y+h, x:x+w]

            # Guardar la región de la placa como una imagen separada
            cv2.imwrite("placa_region.jpg", placa_region)

            # Dibujar el contorno de la placa en verde
            cv2.drawContours(imagen, [placa_contorno], -1, (0, 255, 0), 3)

            return imagen
        else:
            print('No se pudo identificar la placa en la imagen.')
            return None
