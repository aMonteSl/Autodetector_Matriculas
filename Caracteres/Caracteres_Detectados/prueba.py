import pytesseract as tess
from PIL import Image

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specify the path to the image file
path = 'caracter_4.png'

# Open the image using PIL
my_image = Image.open(path)

# Convert the image to binary (black and white)
binary_image = my_image.convert('1')  # '1' corresponds to 1-bit pixels, black and white

# Perform OCR on the binary image
txt = tess.image_to_string(binary_image)

# Print the detected text
print("La matricula detectada es:", txt)
