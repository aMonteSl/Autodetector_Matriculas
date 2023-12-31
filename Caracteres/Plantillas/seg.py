import cv2
import os

def main(input_image_path, output_folder_path):
    # Obtener la ruta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa para la imagen de entrada y la carpeta de salida
    input_image_path = os.path.join(script_dir, input_image_path)
    output_folder_path = os.path.join(script_dir, output_folder_path)

    # Cargar la imagen
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Aplicar umbral para convertir la imagen en blanco y negro
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos en la imagen
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterar a través de cada contorno y guardar la imagen recortada
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        digit_image = image[y:y + h, x:x + w]

        # Guardar la imagen recortada
        output_path = os.path.join(output_folder_path, f"digit_{i + 1}.png")
        cv2.imwrite(output_path, digit_image)

        # Dibujar el bounding box en la imagen original (opcional)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Guardar la imagen original con bounding boxes dibujados (opcional)
    cv2.imwrite(os.path.join(output_folder_path, "output_image.png"), image)

if __name__ == "__main__":
    input_image_path = "PlantillasLetras.jpg"
    output_folder_path = "./"
    main(input_image_path, output_folder_path)

