# import the necessary packages
import numpy as np
import os
import cv2
from keras import models, optimizers, layers, regularizers
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.utils import to_categorical
import random
from imutils import paths
import cv2


class Classify:
    def __init__(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (150, 150))
        img = img.astype("float") / 255.0
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        # print(img)
        self.image = img
        MODEL_DIR = "./static/model"
        self.model_path = os.path.join(MODEL_DIR,"plant_seed_10_layers_using_elu_dropout_2_epoch_50_64_.h5")
        print(os.path.exists(self.model_path))

    def predict(self):
        print("Loading Model")
        print(type(self.model_path))
        # model = models.load_model(self.model_path)
        print("Model Loaded")
        # (planting, growing, flowering, fruiting) = model.predict(self.image)[0]
        print("Loading Model")
        # print(planting)
        # print(growing)
        # print(flowering)
        # print(fruiting)

    @classmethod
    def class_prediction(cls, save_path, api_key):
        class_finder = cls(save_path)
        class_finder.predict()
        pass
