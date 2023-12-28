import cv2
import os

class DecisionChar:
    def __init__(self, tmp_numbers_dirc, char_dirc):
        self.tmp_numbers_dirc = tmp_numbers_dirc
        self.char_dirc = char_dirc
        self.threshold_value = 0  # Puedes ajustar este valor según sea necesario

    def load_templates(self):
        templates = {}
        for file_name in os.listdir(self.tmp_numbers_dirc):
            if file_name.endswith('.jpg'):
                template_path = os.path.join(self.tmp_numbers_dirc, file_name)
                number_label = os.path.splitext(file_name)[0]
                number_template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                templates[number_label] = number_template
        return templates

    def calculate_similarity(self, img1, img2):
        # Umbralizar con Otsu
        _, img1_thresh = cv2.threshold(img1, self.threshold_value, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, img2_thresh = cv2.threshold(img2, self.threshold_value, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Calcular la similitud (porcentaje de píxeles coincidentes)
        similarity_percentage = (cv2.bitwise_and(img1_thresh, img2_thresh).sum() / 255) / img1.size

        return similarity_percentage

    def start(self, detected_char):
        templates = self.load_templates()

        best_match_label = None
        best_similarity = 0

        # Iterar sobre cada número y calcular la similitud con el dígito detectado
        for number_label, number_template in templates.items():
            similarity = self.calculate_similarity(detected_char, number_template)
            
            # Actualizar si encontramos un número con mayor similitud
            if similarity > best_similarity:
                best_similarity = similarity
                best_match_label = number_label

        # Imprimir la etiqueta del número con mejor similitud y el valor de similitud
        print(f"Mejor coincidencia: Número {best_match_label}, Similitud: {best_similarity}")

        #return best_match_label if best_match_label is not None else 'Desconocido'