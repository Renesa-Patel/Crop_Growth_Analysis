import cv2
import numpy as np

class Color_Identifer:
    def __init__(self, path):
        img = cv2.imread(path)
        self.image = img
        self.image_hsl = None

    def resize(self, width=None, height=None, inter=cv2.INTER_AREA):
        (h, w) = self.image.shape[:2]
        if width is None and height is None:
            return self.image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        self.image = cv2.resize(self.image, dim, inter)

    def color_total_pixels(self, fore_rect=(0, 350, 400, 700)):
        mask = np.zeros(self.image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        # rect is the rectangle to define a foreground image
        # We will configure it in database and define the maximum hegith of the plants in the image

        cv2.grabCut(self.image, mask, fore_rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        self.image = self.image * mask2[:, :, np.newaxis]
        # print(self.image)
        self.image_hsl = cv2.cvtColor(self.image, cv2.COLOR_BGR2HLS)
        # print(self.image)
        count = cv2.countNonZero(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY))
        self.total = count
        return count

    def count_pixels(self, min_threshold=[45, 10, 20], max_threshold=[150, 250, 250]):
        (i, j, k) = (0, 0, 0)
        c_min_threshold = [min_threshold[0] - i, min_threshold[1] - j, min_threshold[2] - k]
        c_max_threshold = [max_threshold[0] + i, max_threshold[1] + j, max_threshold[2] + k]
        MIN = np.array(c_min_threshold, np.uint8)
        MAX = np.array(c_max_threshold, np.uint8)
        dst = cv2.inRange(self.image_hsl, MIN, MAX)
        no_of_pixel = cv2.countNonZero(dst)
        return no_of_pixel

    def data_of_pixels(self):
        threshold_min = [0, 20, 20]
        threshold_max = [45, 240, 240]
        count_h = {}
        count_percent = {}
        sum = 0
        for threshold_max[0] in range(45, 361, 45):
            name = str(threshold_min[0]) + "_" + str(threshold_max[0])
            count_h[name] = self.count_pixels(threshold_min, threshold_max)
            count_percent[name] = (count_h[name] / self.total) * 100
            threshold_min[0] = threshold_min[0] + 45
            sum = sum + count_h[name]

        return count_percent

    def data_of(self, thre=0):
        threshold_min = [0, 0, 0]
        threshold_max = [10, 10, 10]
        count_h = {}
        for threshold_max[0] in range(10, 361, 10):
            for threshold_max[1] in range(10, 101, 10):
                for threshold_max[2] in range(10, 101, 10):
                    g_min = np.array(threshold_min, np.uint8)
                    g_max = np.array(threshold_max, np.uint8)
                    dst1 = cv2.inRange(self.image_hsl, g_min, g_max)
                    name = "H_" + str(threshold_min[0]) + "_" + str(threshold_max[0]) + "_L_" + str(
                        threshold_min[1]) + "_" + str(threshold_max[1]) + "_S_" + str(threshold_min[2]) + "_" + str(
                        threshold_max[2])
                    count_h[name] = cv2.countNonZero(dst1)
                    threshold_min[2] = threshold_min[2] + 10
                threshold_min[2] = 0
                threshold_max[2] = 10
                threshold_min[1] = threshold_min[1] + 10
            threshold_min[1] = 0
            threshold_max[1] = 10
            threshold_min[0] = threshold_min[0] + 10

    def calc_percent(self):
        try:
            self.resize(400)
            total = float(self.color_total_pixels())
            green = float(self.count_pixels())
            percent = float(green / total) * 100
            return percent
        except cv2.error as e:
            pass

    @classmethod
    def execute_color_model(cls, save_path, api_key):
        color_finder = cls(save_path)
        percentage = color_finder.calc_percent()
        data_of = color_finder.data_of_pixels()
        data_of['green_percent'] = percentage
        return data_of