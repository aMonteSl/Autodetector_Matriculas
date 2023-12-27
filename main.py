from detector_matriculas import LPR
import cv2

lpr = LPR()
image = cv2.imread("matricula.jpg")
processed_image = lpr.read_license(image)

if processed_image is not None:
    cv2.imshow("Processed Image", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No license plate found")

