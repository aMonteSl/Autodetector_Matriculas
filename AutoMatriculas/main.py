from detector_placa import PlacaDetector as pld
from segmentacion_placas import PlacaRegionProcessor as prp
from detectar_region import detectar_letra
import cv2

def main():
    detector = pld()
    imagen_resultado = detector.detectar_placa("matricula2.jpg")

    if imagen_resultado is not None:
        cv2.imshow('Imagen con Placa Detectada', imagen_resultado)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        processor = prp()
        placa_nation = processor.procesar_placa_region("placa_region.jpg")

        # Mostrar las imágenes generadas
        if placa_nation is not None:
            cv2.imshow('Placa Nation', placa_nation)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            placa_nation = cv2.imread("placa_nation.jpg")

            letra = detectar_letra(placa_nation)

            print("Letra detectada: {}".format(letra))

if __name__ == '__main__':
    main()
