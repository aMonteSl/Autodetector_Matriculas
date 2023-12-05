import cv2
import numpy as np

def procesar_imagen(imagen):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Aplicar suavizado Gaussiano
    suavizado = cv2.GaussianBlur(gris, (5,5), 0)
    
    return suavizado

def segmentar_imagen(imagen):
    # Detectar bordes usando Canny
    bordes = cv2.Canny(imagen, 50, 150)
    
    # Realizar una dilatación y erosión para cerrar los huecos en los bordes
    dilatada = cv2.dilate(bordes, None, iterations=2)
    erosionada = cv2.erode(dilatada, None, iterations=1)
    
    return erosionada

def detectar_contornos(imagen):
    contornos, _ = cv2.findContours(imagen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contornos

def estimar_placa(contornos):
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area > 2000:
            peri = cv2.arcLength(cnt, True)
            aprox = cv2.approxPolyDP(cnt, 0.06 * peri, True)
            if len(aprox) == 4:
                return aprox
    return None

def main():
    imagen = cv2.imread('matricula2.jpg')
    procesada = procesar_imagen(imagen)
    segmentada = segmentar_imagen(procesada)
    contornos = detectar_contornos(segmentada)
    placa = estimar_placa(contornos)
    
    if placa is not None:
        cv2.drawContours(imagen, [placa], -1, (0, 255, 0), 3)
        cv2.imshow('Placa detectada', imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('No se pudo detectar la placa del coche.')

if __name__ == '__main__':
    main()