import numpy as np
import cv2
import skimage

class LicensePlateReader:
    def __init__(self, min_area=5000, max_area=50000, min_ratio=3.5, max_ratio=4.95):
        """
        Initializes the LicensePlateReader object with default parameters.

        Args:
            min_area (int): Minimum area for candidate contours.
            max_area (int): Maximum area for candidate contours.
            min_ratio (float): Minimum aspect ratio for candidate contours.
            max_ratio (float): Maximum aspect ratio for candidate contours.
        """
        self.min_area = min_area
        self.max_area = max_area
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def grayscale(self, img):
        """
        Converts the image to grayscale and applies blur.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Grayscale and blurred image.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3, 3))
        return gray

    def apply_threshold(self, img):
        """
        Applies binary inverse threshold to the image.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Thresholded image.
        """
        return cv2.threshold(img, 170, 255, cv2.THRESH_BINARY_INV)[1]

    def apply_adaptive_threshold(self, img):
        """
        Applies adaptive threshold to the image.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Thresholded image.
        """
        if img.ndim == 3:
            img = self.grayscale(img)
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)

    def find_contours(self, img):
        """
        Finds contours in the image.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            list: List of contours.
        """
        return cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    def filter_candidates(self, contours):
        """
        Filters candidate contours based on area and aspect ratio.

        Args:
            contours (list): List of contours.

        Returns:
            list: Filtered list of candidate contours.
        """
        candidates = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)

            epsilon = 0.009 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) < 10 and self.min_area < area < self.max_area:
                aspect_ratio = float(w) / h
                if self.min_ratio < aspect_ratio < self.max_ratio:
                    candidates.append(cnt)
        return candidates

    def get_lowest_candidate(self, candidates):
        """
        Gets the candidate with the lowest y-coordinate.

        Args:
            candidates (list): List of candidate contours.

        Returns:
            numpy.ndarray: Contour with the lowest y-coordinate.
        """
        ys = [cv2.boundingRect(cnt)[1] for cnt in candidates]
        return candidates[np.argmax(ys)]

    def crop_license_plate(self, img, license_contour, margin=3):
        """
        Crops the license plate region from the original image with an expanded margin.

        Args:
            img (numpy.ndarray): Original image.
            license_contour (numpy.ndarray): Contour of the license plate.
            margin (int): Margin to expand the crop (pixels).

        Returns:
            numpy.ndarray: Cropped image of the license plate region with expanded margin.
        """
        x, y, w, h = cv2.boundingRect(license_contour)
        x_expanded = max(0, x - margin)
        y_expanded = max(0, y - margin)
        w_expanded = min(img.shape[1] - x_expanded, w + 2 * margin)
        h_expanded = min(img.shape[0] - y_expanded, h + 2 * margin)
        cropped_license_plate = img[y_expanded:y_expanded + h_expanded, x_expanded:x_expanded + w_expanded]
        return cropped_license_plate

    def close_and_open(self, img):
        """
        Applies morphological closing and opening operations to the image.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Image after closing and opening operations.
        """
        kernel = np.ones((3, 3), np.uint8)
        closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        closed = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return closed

    def clear_border(self, img):
        """
        Clears the border of the image using skimage.segmentation.clear_border.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Image with cleared border.
        """
        return skimage.segmentation.clear_border(img)

    def invert_image(self, img):
        """
        Inverts the colors of the image.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Inverted image.
        """
        return cv2.bitwise_not(img)

    def draw_contours(self, img, contours):
        """
        Draws contours on the original image.

        Args:
            img (numpy.ndarray): Original image.
            contours (list): List of contours.

        Returns:
            numpy.ndarray: Image with drawn contours.
        """
        return cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)

    def read_license(self, img):
        """
        Main method for reading the license plate. Processes the image, detects contours, filters candidates,
        and returns the final processed image.

        Args:
            img (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray or str: Processed image or an error message if no license plate is found.
        """
        gray = self.grayscale(img)
        thresh = self.apply_threshold(gray)
        contours = self.find_contours(thresh)
        candidates = self.filter_candidates(contours)

        img_with_contours = self.draw_contours(img, candidates)
        cv2.imshow("Detected Contours", img_with_contours)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if candidates:
            license_contour = candidates[0]
            if len(candidates) > 1:
                license_contour = self.get_lowest_candidate(candidates)

            cropped_license_plate = self.crop_license_plate(img, license_contour)
            gray_cropped = self.grayscale(cropped_license_plate)
            thresh_cropped = self.apply_adaptive_threshold(gray_cropped)

            # Close and open operations
            close_open = self.close_and_open(thresh_cropped)

            # Clear the border of the resulting image
            clear_border = self.clear_border(close_open)

            # Invert the colors of the final image
            final_image = self.invert_image(clear_border)

            return final_image
        else:
            return "No license plate found"

# Example usage:
if __name__ == "__main__":
    lpr = LicensePlateReader()
    image_path = "path/to/your/image.jpg"
    image = cv2.imread(image_path)

    result = lpr.read_license(image)
    if isinstance(result, np.ndarray):
        cv2.imshow("Processed License Plate", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(result)
