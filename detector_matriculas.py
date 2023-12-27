import numpy as np
import cv2
import skimage

class LPR:
    def __init__(self, min_area=8000, max_area=50000, min_ratio=4.05, max_ratio=4.6):
        self.min_area = min_area
        self.max_area = max_area
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def grayscale(self, img):
        # Convierte la imagen a escala de grises
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def apply_threshold(self, img):
        # Aplica umbral binario inverso a la imagen
        return cv2.threshold(img, 170, 255, cv2.THRESH_BINARY_INV)[1]

    def apply_adaptive_threshold(self, img):
        # Aplica umbral adaptativo a la imagen
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)

    def find_contours(self, img):
        # Encuentra contornos en la imagen
        return cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    def filter_candidates(self, contours):
        candidates = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)

            # Aproximación de contorno para obtener el número de vértices
            epsilon = 0.009 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) < 10 and self.min_area < area < self.max_area:
                print('Área:', area)
                print('Número de vértices:', len(approx))
                aspect_ratio = float(w) / h
                print('Relación de aspecto:', aspect_ratio)
                
                # Verifica la relación de aspecto
                if self.min_ratio < aspect_ratio < self.max_ratio:
                    candidates.append(cnt)
        return candidates

    def get_lowest_candidate(self, candidates):
        ys = []
        for cnt in candidates:
            x, y, w, h = cv2.boundingRect(cnt)
            ys.append(y)
        return candidates[np.argmax(ys)]

    def crop_license_plate(self, img, license):
        x, y, w, h = cv2.boundingRect(license)
        # Recorta la región de la matrícula de la imagen original
        return img[y:y+h, x:x+w]
    

    def closed_license_plate(self, thresh_cropped):
        # Operación de cierre con un elemento estructurante (9x9)
        kernel = np.ones((9, 9), np.uint8)
        closed = cv2.morphologyEx(thresh_cropped, cv2.MORPH_CLOSE, kernel)
        return closed

    def clear_border(self, img):
        # Elimina los bordes de la imagen
        return skimage.segmentation.clear_border(img)

    def invert_image(self, img):
        # Invierte los colores de la imagen
        return cv2.bitwise_not(img)

    def read_license(self, img, psm=7):
        gray = self.grayscale(img)
        thresh = self.apply_threshold(gray)
        contours = self.find_contours(thresh)
        candidates = self.filter_candidates(contours)

        if candidates:
            license = candidates[0]
            if len(candidates) > 1:
                license = self.get_lowest_candidate(candidates)

            cropped = self.crop_license_plate(gray, license)
            thresh_cropped = self.apply_adaptive_threshold(cropped)
            
            closed = self.closed_license_plate(thresh_cropped)

            # Elimina los bordes de la imagen resultante
            clear_border = self.clear_border(closed)

            # Invierte los colores de la imagen final
            final = self.invert_image(clear_border)

            return final
        else:
            return "No license plate found"

        '''if candidates:
            license = candidates[0]
            if len(candidates) > 1:
                license = self.get_lowest_candidate(candidates)
            #cropped = self.crop_license_plate(gray, license)
            #thresh_cropped = self.apply_adaptive_threshold(cropped)
            #clear_border = self.clear_border(thresh_cropped)
            #final = self.invert_image(clear_border)
            return contours
        else:
            return "No license plate found"'''
        

        #Antiguo filtro de contornos
        '''x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if (np.isclose(aspect_ratio, self.ratio, atol=0.7) and
               (self.max_w > w > self.min_w) and
               (self.max_h > h > self.min_h)):
                candidates.append(cnt)'''