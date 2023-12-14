import cv2
import numpy as np

def remove_highlights(image):
    # Aplicar un filtro de mediana para eliminar brillos y reflejos
    median_filtered = cv2.medianBlur(image, 9)
    return median_filtered

def find_and_apply_rectangle(image_path, threshold, min_area_threshold):
    # Cargar la imagen a color
    color_image = cv2.imread(image_path)

    if color_image is None:
        raise Exception(f'Error: No se puede leer la imagen {image_path}')

    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # Eliminar brillos y reflejos con un filtro de mediana
    filtered_image = remove_highlights(gray_image)

    # Obtener el histograma de la imagen filtrada
    hist, _ = np.histogram(filtered_image.flatten(), bins=256, range=[0, 256])

    # Calcular el umbral exigente basado en el histograma
    cumulative_sum = np.cumsum(hist)
    threshold_value = np.argmax(cumulative_sum > threshold * cumulative_sum[-1])

    # Binarizar la imagen filtrada utilizando el umbral calculado
    binary_image = (filtered_image > threshold_value).astype(np.uint8) * 255

    # Mostrar la imagen binaria después de la umbralización
    cv2.imshow('Binary Image', binary_image)
    cv2.waitKey(0)

    # Aplicar operación de cierre más agresiva a la imagen binaria
    kernel_large = np.ones((9, 9), np.uint8)
    binary_image_closed = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel_large)

    # Mostrar la imagen binaria después de la apertura y cierre
    cv2.imshow('Binary Image (After Closing)', binary_image_closed)
    cv2.waitKey(0)

    # Encontrar contornos en la imagen binaria después del cierre
    contours, _ = cv2.findContours(binary_image_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Buscar un rectángulo blanco con área mínima
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Verificar si el contorno es un rectángulo con cuatro vértices
            if len(approx) == 4:
                # Dibujar el rectángulo encontrado en la imagen a color
                cv2.drawContours(color_image, [approx], 0, (255, 0, 255), 2)

                # Mostrar la imagen a color con el rectángulo encontrado
                cv2.imshow('Rectangle Found in Color Image', color_image)
                cv2.waitKey(0)

                break

# Especifica la ruta de la imagen a color
color_image_path = 'matricula6.jpg'

# Establece el umbral exigente y el área mínima para el rectángulo blanco
threshold = 0.65
min_area_threshold = 10000  # Ajusta según sea necesario

# Llama a la función para buscar y aplicar el rectángulo en la imagen a color
try:
    find_and_apply_rectangle(color_image_path, threshold, min_area_threshold)
except Exception as e:
    print(f'Error: {e}')
    print('No se encontró la imagen')











