import cv2
import numpy as np


class ImagePreprocessor:

    def __init__(self, img):
        self.img = img
        self.gray_img = None
        self.threshold = None
        self.counter = 0

    def check_image_size(self):
        if min(self.img.shape[:2]) < 300:
            raise Exception(
                "Image is too small. Please provide an image with at least 300x300 resolution."
            )

    def check_brightness(self):
        brightness = cv2.mean(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))[0]
        print("Brightness:", brightness)

    def check_noise(self):
        noise = cv2.meanStdDev(cv2.cvtColor(self.threshold,
                                            cv2.COLOR_BGR2GRAY))[1][0][0]
        print("Noise:", noise)

    def resize_image(self):
        aspect_ratio = self.img.shape[0] / self.img.shape[1]
        target_height = 1000
        if self.img.shape[0] < target_height:
            target_width = int(target_height / aspect_ratio)
            self.img = cv2.resize(self.img, (target_width, target_height),
                                  interpolation=cv2.INTER_CUBIC)

    def check_image_blurriness(self):
        score = cv2.Laplacian(self.gray_img, cv2.CV_64F).var()
        # print(score)
        # var = cv2.meanStdDev(score)[1] ** 2
        # print('Blurriness:', var[0])
        # if score < 10:
        #     raise Exception('Image is too Blurry')
        if score < 150 and self.counter < 2:
            self.counter += 1
            self.remove_blur()
            self.check_image_blurriness()

    def remove_blur(self):
        # Apply Canny edge detection
        edges = cv2.Canny(self.gray_img, 100, 200)

        # Apply Gaussian blur to the edges
        blur = cv2.GaussianBlur(edges, (5, 5), 0)

        # Subtract the blurred edges from the original image
        self.gray_img = cv2.addWeighted(self.gray_img, 1.5, blur, -0.5, 0)

    def convert_to_grayscale(self):
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def convert_to_colour(self):
        self.img = cv2.cvtColor(self.gray_img, cv2.COLOR_GRAY2BGR)

    def convert_to_colour(self):
        self.img = cv2.cvtColor(self.gray_img, cv2.COLOR_GRAY2BGR)

    def check_contrast(self):
        # Calculate the contrast
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(self.gray_img)
        contrast = maxVal - minVal
        print("Contrast:", contrast)

    def perform_otsu_threshold(self):
        _, self.threshold = cv2.threshold(
            self.gray_img, 20, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    def improve_image_quality(self):
        kernel = np.ones((3, 3), np.uint8)
        self.threshold = cv2.morphologyEx(self.threshold, cv2.MORPH_CLOSE,
                                          kernel)
        self.threshold = cv2.morphologyEx(self.threshold, cv2.MORPH_OPEN,
                                          kernel)

    def remove_noise(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        self.threshold = cv2.morphologyEx(self.threshold, cv2.MORPH_CLOSE,
                                          kernel)

    def remove_horizontal_lines(self):
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
        self.threshold = cv2.morphologyEx(self.threshold,
                                          cv2.MORPH_OPEN,
                                          horizontal_kernel,
                                          iterations=2)

    def remove_vertical_lines(self):
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
        self.threshold = cv2.morphologyEx(self.threshold,
                                          cv2.MORPH_OPEN,
                                          vertical_kernel,
                                          iterations=2)

    def erode_image(self):
        kernel = np.ones((3, 3), np.uint8)
        self.threshold = cv2.erode(self.threshold, kernel, iterations=1)

    def dilate_image(self):
        kernel = np.ones((3, 3), np.uint8)
        self.threshold = cv2.dilate(self.threshold, kernel, iterations=1)

    def remove_small_objects(self):
        contours, _ = cv2.findContours(self.threshold, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 50:
                cv2.drawContours(self.threshold, [contour], -1, (0, 0, 0), -1)

    def reduce_brightness(self):
        # Reduce brightness by multiplying each pixel value by a factor less than 1
        brightness_factor = 0.5
        self.threshold = cv2.multiply(self.threshold, brightness_factor)

    def divide_half_horizontal(self):
        # this is horizontal division
        h, w, c = self.img.shape
        half2 = h // 2

        top_half = self.img[:half2, :]
        bottom_half = self.img[half2 + 150:, :]

        return top_half, bottom_half

    def process(self):
        self.check_image_size()
        self.resize_image()
        # self.check_brightness()

        self.convert_to_grayscale()
        # aspect_ratio = self.gray_img.shape[0] / self.gray_img.shape[1]
        # target_height = 500
        # target_width = int(target_height / aspect_ratio)
        # sample = cv2.resize(self.gray_img, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('converting to grayScale 1', sample)

        self.check_image_blurriness()
        # aspect_ratio = self.gray_img.shape[0] / self.gray_img.shape[1]
        # target_height = 500
        # target_width = int(target_height / aspect_ratio)
        # sample = cv2.resize(
        #     self.gray_img, (target_width, target_height), interpolation=cv2.INTER_CUBIC
        # )
        # cv2.imshow("After checking blurness 2", sample)

        # self.check_contrast()

        self.perform_otsu_threshold()
        # aspect_ratio = self.threshold.shape[0] / self.threshold.shape[1]
        # target_height = 600
        # target_width = int(target_height / aspect_ratio)
        # sample = cv2.resize(
        #     self.threshold, (target_width, target_height), interpolation=cv2.INTER_CUBIC
        # )
        # cv2.imshow("OTSU 3", sample)

        # # self.check_noise()

        # self.remove_noise()
        # aspect_ratio = self.threshold.shape[0] / self.threshold.shape[1]
        # target_height = 600
        # target_width = int(target_height / aspect_ratio)
        # sample = cv2.resize(self.threshold, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('Aft noise reduce 5', sample)

        self.improve_image_quality()
        # aspect_ratio = self.threshold.shape[0] / self.threshold.shape[1]
        # target_height = 400
        # target_width = int(target_height / aspect_ratio)
        # sample = cv2.resize(self.threshold, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('After improve of image quality5', sample)

        # self.remove_small_objects()
        # aspect_ratio = self.threshold.shape[0] / self.threshold.shape[1]
        # target_height = 600
        # target_width = int(target_height / aspect_ratio)
        # sample = cv2.resize(self.threshold, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('After small objects removes 6', sample)

        # if self.counter > 4:
        #     self.dilate_image()
        #     self.dilate_image()
        #     self.dilate_image()
        # elif self.counter > 3:
        #     self.dilate_image()

        # self.erode_image()

        # # # self.reduce_brightness()
        # cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self.threshold


def image_preprocessor(img):
    preprocessor = ImagePreprocessor(img)
    return preprocessor.process()
