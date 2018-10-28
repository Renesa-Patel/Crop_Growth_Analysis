import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
# import colorsys
import cv2

# # (1) Import the file to be analyzed!
# img_file = Image.open("thedress.jpg")
# img = img_file.load()
img = cv2.imread('D:\\Renesa\\4th Year IT\\SEM_7\\Computer_Vision\\Practical\\Plant_stage\\Nagaraju_PVB0020028\\A7238796121robo1531237603406.jpg')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
# (2) Get image width & height in pixels
[ys, xs] = img.shape[:2]
# xs = xs - 1
# ys = ys - 1
max_intensity = 100
hues = {}

# (3) Examine each pixel in the image file
for x in range(0, xs):
    for y in range(0, ys):
        # (4)  Get the RGB color of the pixel
        [b, g, r] = img[y, x]
        [h, s, v] = img_hsv[y, x]
        # (5)  Normalize pixel color values
        r /= 255.0
        g /= 255.0
        b /= 255.0

        # (6)  Convert RGB color to HSV
        # [h, s, v] = colorsys.rgb_to_hsv(r, g, b)

        # (7)  Marginalize s; count how many pixels have matching (h, v)
        if h not in hues:
            hues[h] = {}
        if v not in hues[h]:
            hues[h][v] = 1
        else:
            if hues[h][v] < max_intensity:
                hues[h][v] += 1

# (8)   Decompose the hues object into a set of one dimensional arrays we can use with matplotlib
h_ = []
v_ = []
i = []
colours = []

for h in hues:
    for v in hues[h]:
        h_.append(h)
        v_.append(v)
        i.append(hues[h][v])
        [b, g, r] = cv2.cvtColor(np.array([int(h), int(s), int(v)], np.uint8), cv2.COLOR_HSV2BGR)
        colours.append([b, g, r])

# (9)   Plot the graph!
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.scatter(h_, v_, i, s=5, c=colours, lw=0)

ax.set_xlabel('Hue')
ax.set_ylabel('Value')
ax.set_zlabel('Intensity')
fig.add_axes(ax)
plt.show()


def count_pixels(image, min_threshold=[52, 89, 76], max_threshold=[52, 89, 76]):
    (i, j, k) = (20, 30, 20)
    c_min_threshold = [min_threshold[0] - i, min_threshold[1] - j, min_threshold[2] - k]
    c_max_threshold = [max_threshold[0] + i, max_threshold[1] + j, max_threshold[2] + k]
    MIN = np.array(c_min_threshold, np.uint8)
    MAX = np.array(c_max_threshold, np.uint8)
    dst = cv2.inRange(image, MIN, MAX)
    no_of_pixel = cv2.countNonZero(dst)
    total = cv2.countNonZero(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    return [no_of_pixel, total, (no_of_pixel/total)*100]

img = cv2.imread('D:\\Renesa\\4th Year IT\\SEM_7\\Computer_Vision\\Practical\\Plant_stage\\Nagaraju_PVB0020028\\A7238796121robo1531237603406.jpg')
rt = count_pixels(img)
print(rt)