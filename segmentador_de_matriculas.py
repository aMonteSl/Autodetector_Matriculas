from detector_matriculas import LPR
from detector_caracteres import SegmentatorChars as SGC
from decisor_caracteres import DecisionChar as DC
import cv2
import os

# Dimensiones deseadas
DESIRED_HEIGHT = 1069
DESIRED_WIDTH = 1900

IMAGE_DIRECTORY = 'Imagenes_coches'
DETECTED_DIRECTORY = 'matriculas_detectadas'
USER_INPUTS_FILE = 'user_inputs.txt'
LETRAS_PLANTILLAS = 'Caracteres/Plantillas/Letras'
NUMEROS_PLANTILLAS = 'Caracteres/Plantillas/Numeros'
CARACTERES_DECIDIR = 'Caracteres/Caracteres_Detectados'

lpr = LPR()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def segmentation_chars(processed_image):
    sgc = SGC(processed_image)
    sgc.start()

def decision_caracteres():
    char = DC(NUMEROS_PLANTILLAS, CARACTERES_DECIDIR)
    char.start()


def process_image():
    with open(os.path.join(DETECTED_DIRECTORY, USER_INPUTS_FILE), 'w') as user_inputs_file:
        user_inputs_file.write("")

    while True:
        clear_terminal()

        available_images = sorted([file for file in os.listdir(IMAGE_DIRECTORY) if file.lower().endswith('.jpg')],
                                key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else float('inf'))

        print("Imágenes disponibles:")
        for i, image in enumerate(available_images, start=1):
            print(f"{i}. {image}")

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

        image_path = os.path.join(IMAGE_DIRECTORY, selected_image)
        image = cv2.imread(image_path)

        if image is not None and (image.shape[0] > DESIRED_HEIGHT or image.shape[1] > DESIRED_WIDTH):
            image = cv2.resize(image, (DESIRED_WIDTH, DESIRED_HEIGHT))

        if image is not None:
            height, width = image.shape[:2]
            print(f"Dimensiones de la imagen: Altura = {height}, Ancho = {width}")

            processed_image = lpr.read_license(image)

            if isinstance(processed_image, str):
                print(processed_image)
            else:
                if not os.path.exists(DETECTED_DIRECTORY):
                    os.makedirs(DETECTED_DIRECTORY)

                matricula_number = choice
                output_filename = f"matricula{matricula_number}.jpg"
                output_path = os.path.join(DETECTED_DIRECTORY, output_filename)

                cv2.imwrite(output_path, processed_image)
                print(f"La imagen procesada ha sido guardada como {output_filename}")

                with open(os.path.join(DETECTED_DIRECTORY, USER_INPUTS_FILE), 'a') as user_inputs_file:
                    user_inputs_file.write(f"User choice: {choice}, Selected image: {selected_image}\n")

                cv2.imshow("Processed Image", processed_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                # Segmentación de caracteres
                segmentation_chars(processed_image)

                # Decision de caracteres
                decision_caracteres()

            input("Presiona Enter para continuar...")
        else:
            print("Error al cargar la imagen. Asegúrate de que el archivo existe y tiene el formato correcto.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    process_image()
