import os
import shutil
from license_plate_detector import LicensePlateReader
import cv2

class PlateSegmentation:
    def __init__(self):
        """
        Initializes the PlateSegmentation object with constants and an instance of the LicensePlateReader.
        """
        # Constants
        self.DESIRED_HEIGHT = 1069
        self.DESIRED_WIDTH = 1900
        self.IMAGE_DIRECTORY = 'CarImages'
        self.DETECTED_DIRECTORY = os.path.abspath('DetectedPlates')  # Absolute path for DetectedPlates
        self.USER_INPUTS_FILE = os.path.join(self.DETECTED_DIRECTORY, 'user_inputs.txt')  # Absolute path for user_inputs.txt

        # Clear the content of DetectedPlates before each execution
        if os.path.exists(self.DETECTED_DIRECTORY):
            shutil.rmtree(self.DETECTED_DIRECTORY)
        os.makedirs(self.DETECTED_DIRECTORY)

        # Instance of the LicensePlateReader object
        self.lpr = LicensePlateReader()

    def clear_terminal(self):
        """
        Clears the terminal screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_images(self):
        """
        Loads and displays available images for processing, prompting the user to make a selection.

        Returns:
            tuple: Choice number and selected image filename.
        """
        available_images = sorted([file for file in os.listdir(self.IMAGE_DIRECTORY) if file.lower().endswith('.jpg')],
                                  key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else float('inf'))

        while True:
            self.clear_terminal()
            print("Available images:")
            for i, image in enumerate(available_images, start=1):
                print(f"{i}. {image}")

            user_input = input("Select the number of the image you want to process (or 'EXIT' to exit): ").strip().lower()

            if user_input == 'exit':
                return None, None

            if user_input.isdigit():
                choice = int(user_input)
                if 1 <= choice <= len(available_images):
                    selected_image = available_images[choice - 1]
                    return choice, selected_image

            print("Invalid selection. Make sure to enter a valid number.")
            input("Press Enter to continue...")

    def process_image(self, choice, selected_image, image_path):
        """
        Processes the selected image, displays the result, and saves the processed image.

        Args:
            choice (int): User's choice number.
            selected_image (str): Filename of the selected image.
            image_path (str): Absolute path to the selected image.
        """
        image = cv2.imread(image_path)

        if image is not None and (image.shape[0] > self.DESIRED_HEIGHT or image.shape[1] > self.DESIRED_WIDTH):
            image = cv2.resize(image, (self.DESIRED_WIDTH, self.DESIRED_HEIGHT))

        if image is not None:
            height, width = image.shape[:2]
            print(f"Image dimensions: Height = {height}, Width = {width}")

            processed_image = self.lpr.read_license(image)

            if isinstance(processed_image, str):
                print(processed_image)
            else:
                self.display_and_save_result(processed_image, choice, selected_image)

    def display_and_save_result(self, processed_image, plate_number, selected_image):
        """
        Displays the processed image, saves it, and records user inputs.

        Args:
            processed_image (numpy.ndarray): Processed license plate image.
            plate_number (int): User's choice number.
            selected_image (str): Filename of the selected image.
        """
        if not os.path.exists(self.DETECTED_DIRECTORY):
            os.makedirs(self.DETECTED_DIRECTORY)

        output_filename = f"plate{plate_number}.jpg"
        output_path = os.path.join(self.DETECTED_DIRECTORY, output_filename)

        cv2.imwrite(output_path, processed_image)
        print(f"The processed image has been saved as {output_filename}")

        with open(self.USER_INPUTS_FILE, 'a') as user_inputs_file:
            user_inputs_file.write(f"User choice: {plate_number}, Selected image: {selected_image}. Path: {output_path}\n")

        cv2.imshow("Processed Image", processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def segmentation_of_the_plate(self):
        """
        Main method for plate segmentation. Loads images, processes each image, and allows the user to continue.
        """
        with open(self.USER_INPUTS_FILE, 'w') as user_inputs_file:
            user_inputs_file.write("")

        while True:
            self.clear_terminal()
            choice, selected_image = self.load_images()

            if choice is None:
                break

            image_path = os.path.join(self.IMAGE_DIRECTORY, selected_image)
            self.process_image(choice, selected_image, image_path)
            input("Press Enter to continue...")

# Example usage:
if __name__ == "__main__":
    app = PlateSegmentation()
    app.segmentation_of_the_plate()



