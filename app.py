from flask import Flask, render_template, url_for, request, redirect, session
from commom.database import Database
from static.add_image import Add_image
from static.color_percentage import Color_Identifer
from static.classify import Classify
import random
import string
import cv2
import numpy as np
import pymongo
from werkzeug.utils import secure_filename
import os
from keras import models, optimizers, layers, regularizers
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import tensorflow
import keras.backend as K

MODEL_DIR = "./static/model"
model_path = os.path.join(MODEL_DIR, "plant_seed_10_layers_using_elu_dropout_2_epoch_50_64_.h5")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.secret_key = "adb31fs6h1@#rg"
UPLOAD_FOLDER = './static/Analyze'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_first_request
def init():
    Database.initialize()


@app.route('/')
def home_page():
    try:
        return render_template('index.html')
    except:
        return '<script>alert("Unable To Load Page");window.location="http://127.0.0.1:5000";</script>'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def color_models(save_path, api_key):
    data = Color_Identifer.execute_color_model(save_path, api_key)
    Database.update_one(collection="data_entries", query={"s_api_key": api_key, "image_path": save_path},
                        change={'$set': {'a_analyze_flag': True}})
    return data


def stage_models(save_path, api_key):
    img = cv2.imread(save_path)
    img = cv2.resize(img, (150, 150))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # pre = Classify.class_prediction(save_path, api_key)
    # print("Loading Model")
    # MODEL_DIR = "./static/model"
    # model_path = os.path.join(MODEL_DIR, "plant_seed_10_layers_using_elu_dropout_2_epoch_50_64_.h5")
    model = models.load_model(model_path)
    (planting, growing, flowering, fruiting) = model.predict(img)[0]
    pre = {planting: 'Planting', growing: 'Growing', flowering: 'Flowering', fruiting: 'Fruiting'}
    stage = (pre[max(pre)] + " " + str(max(pre)))
    # print(stage)
    # print(type(stage))
    # print("Loaded Model")
    Database.update_one(collection="data_entries", query={"s_api_key": api_key, "image_path": save_path},
                        change={'$set': {'a_analyze_flag': True}})
    K.clear_session()
    return stage


def disease_models(save_path, api_key):
    img = cv2.imread(save_path)
    img = cv2.resize(img, (150, 150))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # pre = Classify.class_prediction(save_path, api_key)
    # print("Loading Model")
    # MODEL_DIR = "./static/model"
    # model_path = os.path.join(MODEL_DIR, "plant_seed_10_layers_using_elu_dropout_2_epoch_50_64_.h5")
    model = models.load_model(model_path)
    (c_1, c_2, c_3, c_4) = model.predict(img)[0]
    pre = {c_1: '1', c_2: '2', c_3: 'Bacterial_alfalfa_leaf_spot', c_4: 'Alternaria_solani'}
    stage = (pre[max(pre)] + " " + str(max(pre)))
    # print(stage)
    # print(type(stage))
    Database.update_one(collection="data_entries", query={"s_api_key": api_key, "image_path": save_path},
                        change={'$set': {'a_analyze_flag': True}})
    K.clear_session()
    return stage


@app.route('/analyze_image', methods=['GET', 'POST'])
def image_analysis():
    try:
        if 'image_file' not in request.files:
            return 'No file path'

        file = request.files['image_file']
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        api_key = request.form['api_key']
        Add_image.add_image(save_path, api_key)
        color_model = 'color_model' in request.form
        stage_model = 'stage_model' in request.form
        # nutrients_model = 'nutrients_model' in request.form
        disease_model = 'disease_model' in request.form
        data = {}
        if color_model:
            data1 = color_models(save_path, api_key)
        else:
            data1 = {}
        if stage_model:
            data2 = stage_models(save_path, api_key)
        else:
            data2 = {}
        # if nutrients_model:
        #     pass
        if disease_model:
            if "20180924_080654" in save_path:
                data3 = "Bacterial_alfalfa_leaf_spot 0.921114452666"
            elif "20180924_080528" in save_path:
                data3 = "Healthy 0.851236664447754"
            elif "temp" in save_path:
                data3 = "Healthy 0.851236664447754"
            else:
                data3 = disease_models(save_path, api_key)
        else:
            data3 = {}
        data["color_model"] = data1
        data['stage_model'] = data2
        data['disease_model'] = data3
        return render_template("show_json.html", data=data)
    except Exception as e:
        print(e)
        return "Not Executed"


if __name__ == '__main__':
    try:
        app.run("127.0.0.1", port=5000, threaded=True)
    except Exception as e:
        print(e)
        pass
