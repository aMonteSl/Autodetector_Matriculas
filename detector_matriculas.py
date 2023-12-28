import numpy as np
import cv2
import skimage

class LPR:
    def __init__(self, min_area=5000, max_area=50000, min_ratio=3.5, max_ratio=4.95): #Min ratio 4.05  #Imagenes de lejos min_area=5000, max_area=50000
        self.min_area = min_area
        self.max_area = max_area
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def grayscale(self, img):
        # Convierte la imagen a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray,(3,3))
        return gray
    
    def cannyimg(self, img):
        canny = cv2.Canny(img,150,200)
        canny = cv2.dilate(canny,None,iterations=1)
        return canny

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

            #Aproximación de contorno para obtener el número de vértices
            epsilon = 0.009 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            '''if area > self.min_area:
                print('Área antes de filtro:', area)
                candidates.append(cnt)'''
            if len(approx) < 10 and self.min_area < area < self.max_area:
                #print('---PASO EL PRIMER FILTRO---')
                #print('Área:', area)
                #print('Número de vértices:', len(approx))
                aspect_ratio = float(w) / h
                #print('Relación de aspecto:', aspect_ratio)
                
                # Verifica la relación de aspecto
                if self.min_ratio < aspect_ratio < self.max_ratio:
                    #print('---PASO EL FILTRO POR COMPLETO. ES UNA MATRICULA---')
                    candidates.append(cnt)
                    #print('NUMEROS DE CANDIDATOS TOTALES: ', len(candidates))
                #print('\n\n\n')
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
    

    def open_and_close(self, img):
        # Definir el kernel para las operaciones de apertura y cierre (3x3)
        kernel = np.ones((3, 3), np.uint8)

        # Aplicar la operación de apertura
        opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        # Aplicar la operación de cierre
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

        # Devolver la imagen después de las operaciones de apertura y cierre
        return closed


    def clear_border(self, img):
        # Elimina los bordes de la imagen
        return skimage.segmentation.clear_border(img)

    def invert_image(self, img):
        # Invierte los colores de la imagen
        return cv2.bitwise_not(img)
    
    def draw_contours(self, img, contours):
        # Dibuja los contornos en la imagen original
        return cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)

    def read_license(self, img, psm=7):
        gray = self.grayscale(img)
        canny = self.cannyimg(gray)
        thresh = self.apply_threshold(gray)
        contours = self.find_contours(thresh)
        candidates = self.filter_candidates(contours)

        # Dibujar contornos en la imagen original
        img_with_contours = self.draw_contours(img, candidates)

        # Mostrar la imagen con los contornos
        cv2.imshow("Contornos Detectados", img_with_contours)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if candidates:
            license = candidates[0]
            if len(candidates) > 1:
                license = self.get_lowest_candidate(candidates)

            cropped = self.crop_license_plate(gray, license)
            thresh_cropped = self.apply_adaptive_threshold(cropped)
            
            open_close = self.open_and_close(thresh_cropped)

            # Elimina los bordes de la imagen resultante
            clear_border = self.clear_border(open_close)

            # Invierte los colores de la imagen final
            final = self.invert_image(clear_border)

            return final
        else:
            return "No license plate found"

        '''# Dibujar contornos en la imagen original
        img_with_contours = self.draw_contours(img, contours)

        # Mostrar la imagen con los contornos
        cv2.imshow("Contornos Detectados", img_with_contours)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return None'''

        '''if candidates:
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
            return "No license plate found" '''

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