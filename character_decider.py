import re
import os
import pytesseract
from PIL import Image
import logging

class LicensePlateReader:
    def __init__(self, detected_directory='DetectedPlates', output_file='license_plates_text.txt'):
        """
        Initializes the LicensePlateReader object.

        Args:
            detected_directory (str): Directory for processed images.
            output_file (str): File to store license plate text results.
        """
        # Configure the path to the Tesseract OCR executable (adjust according to your installation)
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

        # Directory for processed images
        self.detected_directory = detected_directory

        # File containing the text of license plates
        self.output_file = output_file

        # Configure logging
        logging.basicConfig(filename='license_plate_reader.log', level=logging.ERROR)

    def read_license_plates(self):
        """
        Reads license plates from processed images and writes the results to a file.
        """
        # Check if the directory exists
        if not os.path.exists(self.detected_directory):
            print(f"Error: The directory '{self.detected_directory}' does not exist.")
            return

        # Get the list of files sorted numerically
        files = sorted([filename for filename in os.listdir(self.detected_directory) if filename.endswith(('.jpg', '.jpeg', '.png'))],
                       key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf'))

        # Create or open the file to store the results
        try:
            with open(self.output_file, 'w') as output_file:
                # Iterate over the sorted files
                for filename in files:
                    image_path = os.path.join(self.detected_directory, filename)

                    # Use pytesseract to read the text from the license plate
                    plate_text = self.read_text_from_image(image_path)

                    # Print the result in the terminal
                    print(f"For {filename}: License plate detected: {plate_text}")

                    # Write the result to the output file
                    output_file.write(f"Image Path: {filename}, Plate Text: {plate_text}\n")

        except Exception as e:
            logging.error(f"Error processing images: {str(e)}")

    def read_text_from_image(self, image_path):
        """
        Reads text from an image using pytesseract.

        Args:
            image_path (str): Path to the image.

        Returns:
            str: Filtered text from the image.
        """
        # Use pytesseract to read the text from the image
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)

            # Filter unwanted characters
            filtered_text = re.sub(r'[^A-Z0-9]', '', text.upper())

            return filtered_text
        except Exception as e:
            logging.error(f"Error processing the image {image_path}: {str(e)}")
            return ""

# Example usage:
if __name__ == "__main__":
    plate_reader = LicensePlateReader()
    plate_reader.read_license_plates()





