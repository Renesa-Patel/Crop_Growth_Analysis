# USAGE
# python image_class.py --model pokedex.model --labelbin lb.pickle --image test3.jpg

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
                help="path to trained model model")
ap.add_argument("-l", "--labelbin", required=True,
                help="path to label binarizer")
ap.add_argument("-i", "--image", required=True,
                help="path to the image")
args = vars(ap.parse_args())

if __name__ == '__main__':
    # load the trained convolutional neural network and the label
    # binarizer
    print("[INFO] loading network...")
    model = load_model(args["model"])
    lb = pickle.loads(open(args["labelbin"], "rb").read())

    imagePath = args["image"]

    image = cv2.imread(imagePath)
    output = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (96, 96))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # classify the input image
    print("[INFO] classifying image...")
    proba = model.predict(image)[0]
    idx = np.argmax(proba)
    # label is var which is the output to the class of the given image
    label = lb.classes_[idx]

    output = imutils.resize(output, width=400)
    cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 0), 2)

    # show the output image
    print("[INFO] {}".format(label))
    cv2.imshow("Output", output)
    cv2.waitKey(0)