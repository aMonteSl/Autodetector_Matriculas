from license_plate_segmenter import PlateSegmentation
from character_decider import LicensePlateReader
import os

# Message for the user
MSG1 = "\nNow we will see the texts of the detected license plates.\n"

def clear_terminal():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slashes():
    """
    Prints a line of dashes to the console.
    """
    length = len(MSG1)
    i = 0
    while i != length:
        print('-', end='')
        i += 1

def next_step():
    """
    Displays a message to the user and waits for Enter to be pressed.
    """
    clear_terminal()
    print_slashes()
    print(MSG1, end='')
    print_slashes()
    input("\nPress Enter to continue...")
    clear_terminal()

if __name__ == "__main__":
    # Instantiate PlateSegmentation to segment license plates
    app = PlateSegmentation()
    app.segmentation_of_the_plate()

    # Display a message and wait for Enter before proceeding to character recognition
    next_step()

    # Instantiate LicensePlateReader to read and print license plates
    plate_reader = LicensePlateReader()
    plate_reader.read_license_plates()