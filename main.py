from detector_matriculas import LPR
import cv2
import os

# Dimensiones deseadas
DESIRED_HEIGHT = 1069
DESIRED_WIDTH = 1900

IMAGE_DIRECTORY = 'Imagenes_coches'
DETECTED_DIRECTORY = 'matriculas_detectadas'
USER_INPUTS_FILE = 'user_inputs.txt'

lpr = LPR()

def clear_terminal():
    # Clear terminal screen command for Windows and Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')

# Limpiar el contenido de user_inputs.txt al principio
with open(os.path.join(DETECTED_DIRECTORY, USER_INPUTS_FILE), 'w') as user_inputs_file:
    user_inputs_file.write("")

while True:
    clear_terminal()

    # Listar las imágenes disponibles en el directorio y ordenarlas alfanuméricamente
    available_images = sorted([file for file in os.listdir(IMAGE_DIRECTORY) if file.lower().endswith('.jpg')],
                              key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else float('inf'))

    # Imprimir las opciones de imágenes disponibles
    print("Imágenes disponibles:")
    for i, image in enumerate(available_images, start=1):
        print(f"{i}. {image}")

    # Solicitar al usuario que elija una opción
    user_input = input("Seleccione el número de la imagen que desea procesar (o 'EXIT' para salir): ").strip().lower()

    if user_input == 'exit':
        break

    try:
        choice = int(user_input)
        selected_image = available_images[choice - 1]
    except (ValueError, IndexError):
        print("Selección inválida. Asegúrate de ingresar un número válido.")
        input("Presiona Enter para continuar...")
        continue

    # Cargar la imagen seleccionada
    image_path = os.path.join(IMAGE_DIRECTORY, selected_image)
    image = cv2.imread(image_path)

    # Redimensionar la imagen si es necesario
    if image is not None and (image.shape[0] > DESIRED_HEIGHT or image.shape[1] > DESIRED_WIDTH):
        image = cv2.resize(image, (DESIRED_WIDTH, DESIRED_HEIGHT))

    # Obtener dimensiones de la imagen
    if image is not None:
        height, width = image.shape[:2]
        print(f"Dimensiones de la imagen: Altura = {height}, Ancho = {width}")

        # Procesar la imagen
        processed_image = lpr.read_license(image)

        if isinstance(processed_image, str):
            print(processed_image)
        else:
            # Crear el directorio si no existe
            if not os.path.exists(DETECTED_DIRECTORY):
                os.makedirs(DETECTED_DIRECTORY)

            # Obtener el número de matrícula introducido por el usuario
            matricula_number = choice

            # Crear el nombre del archivo de salida
            output_filename = f"matricula{matricula_number}.jpg"
            output_path = os.path.join(DETECTED_DIRECTORY, output_filename)

            # Guardar la imagen procesada
            cv2.imwrite(output_path, processed_image)
            print(f"La imagen procesada ha sido guardada como {output_filename}")

            # Guardar la elección del usuario en el archivo user_inputs.txt
            with open(os.path.join(DETECTED_DIRECTORY, USER_INPUTS_FILE), 'a') as user_inputs_file:
                user_inputs_file.write(f"User choice: {choice}, Selected image: {selected_image}\n")

            # Mostrar la imagen procesada
            cv2.imshow("Processed Image", processed_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        input("Presiona Enter para continuar...")
    else:
        print("Error al cargar la imagen. Asegúrate de que el archivo existe y tiene el formato correcto.")
        input("Presiona Enter para continuar...")

