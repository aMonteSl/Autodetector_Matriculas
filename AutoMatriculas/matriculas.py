import cv2

# Parámetros configurables
SIGMA_X = 1
UMBRAL_ADAPTATIVO_BLOCK_SIZE = 19
UMBRAL_ADAPTATIVO_C = 9
AREA_CONTORNO_MINIMA_PLACA = 2000  # Ajustar el área mínima para la detección de la placa
APROX_POLYDP_FACTOR = 0.02  # Reducir el factor de aproximación

def preprocesar_imagen(imagen):
    # Aplicar ecualización del histograma para mejorar el contraste
    img_yuv = cv2.cvtColor(imagen, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    imagen = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # Aplicar suavizado Gaussiano con sigmaX ajustable
    suavizado = cv2.GaussianBlur(imagen, (5, 5), sigmaX=SIGMA_X)
    
    return suavizado

def identificar_placa(contornos):
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, APROX_POLYDP_FACTOR * cv2.arcLength(cnt, True), True)

        # Buscar un objeto rectangular blanco en la imagen
        if len(approx) == 4 and area > AREA_CONTORNO_MINIMA_PLACA:
            return cnt

    return None

def main(jpg):
    # Añadir automáticamente la extensión .jpg si no está presente
    if not jpg.lower().endswith('.jpg'):
        jpg += '.jpg'

    imagen = cv2.imread(jpg)
    if imagen is None:
        print(f'Error: No se puede leer la imagen {jpg}.')
        return

    procesada = preprocesar_imagen(imagen)
    gris = cv2.cvtColor(procesada, cv2.COLOR_BGR2GRAY)

    _, umbral = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)

    contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    placa_contorno = identificar_placa(contornos)
    if placa_contorno is not None:
        x, y, w, h = cv2.boundingRect(placa_contorno)
        placa_region = imagen[y:y+h, x:x+w]

        # Guardar la región de la placa como una imagen separada
        cv2.imwrite("placa_region.jpg", placa_region)

        # Dibujar el contorno de la placa en verde
        cv2.drawContours(imagen, [placa_contorno], -1, (0, 255, 0), 3)

    else:
        print('No se pudo identificar la placa en la imagen.')

    cv2.imshow('Imagen Original', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()  # Añadir esta línea para cerrar la ventana correctamente

if __name__ == '__main__':
    while True:
        jpg = input('Dime el jpg que quieres escanear la matrícula (sin extensión, se añadirá automáticamente .jpg) o pulsa "s" para salir: ')
        if jpg.lower() == 's':
            print('Saliendo...')
            break
        else:
            main(jpg)
