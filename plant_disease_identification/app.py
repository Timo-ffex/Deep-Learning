#!/home/dit/PACKAGES/.ds_env/bin/python3
#C:\PACKAGES\ds_env\Scripts/python3

#%%
from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, flash, session
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)


#%%
# You can also use pretrained model from Keras
# Check https://keras.io/applications/

print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model, plant):
    from keras.preprocessing import image

    IMAGE_SIZE = [224, 224]

    if plant == 'tomato':
        labels = ['Bacterial_spot','Early_blight','Late_blight','Leaf_Mold','Septoria_leaf_spot',
                'Spider_mites Two-spotted_spider_mite','Target_Spot','Tomato_Yellow_Leaf_Curl_Virus',
                'Tomato_mosaic_virus','healthy']
    
    if plant == 'potato':
        labels = ['Early_blight', 'Late_blight', 'healthy']

    if plant == 'pepper':
        labels = ['Bacterial_spot', 'Healthy']

    if plant == 'maize':
        labels = ['Cercospora_leaf_spot Gray_leaf_spot', 'Common_rust', 'Northern_Leaf_Blight', 'healthy']


    if plant == 'cassava':
        labels =  ['cbb', 'cbsd', 'cgm', 'cmd', 'healthy']


    img = image.load_img(img_path, target_size=IMAGE_SIZE)

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.array(x).astype('float32')/255
    x = np.reshape(x, IMAGE_SIZE + [3])
    x = np.expand_dims(x, axis=0)

    result = model.predict(x)
    os.remove(img_path)
    print('deleted ', img_path)
    print()

    what_class = np.argmax(result, axis=-1)
    scale = '{:.2f}'.format(round(result.max(), 2))

    result_label = labels[what_class[0]]
    if result_label.lower() == 'healthy':
        return (f'{plant.title()} leaf is classified HEALTHY with scale of {scale}')

    else:
        return (f'{plant.title()} leaf is infected with {result_label.upper()} with confident scale of {scale}')



PATH = '/media/dit/005EB9025EB8F190/Users/DiT/Downloads/Me/GitHub/Pylingo/Jupyters/DS/Keras/saved_model/'
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', page='home')

    
@app.route('/tomato', methods=['GET', 'POST'])
def tomato():
    plant = 'tomato'
    session['plant'] = plant
    session['path'] = PATH + 'plant_models/tomato_inception_v3.h5'
    return render_template('tomato.html', title=plant)


@app.route('/pepper', methods=['GET'])
def pepper():
    plant = 'pepper'
    session['plant'] = plant
    session['path'] = PATH + 'plant_models/pepper_inception_v3.h5'
    return render_template('pepper.html', title=plant)


@app.route('/potato', methods=['GET'])
def potato():
    plant = 'potato'
    session['plant'] = plant
    session['path'] = PATH + 'plant_models/potato_inception_v3.h5'
    return render_template('potato.html', title=plant)

@app.route('/maize', methods=['GET'])
def maize():
    plant = 'maize'
    session['plant'] = plant
    session['path'] = PATH + 'plant_models/maize_inception_v3.h5'
    return render_template('maize.html', title=plant)

@app.route('/cassava', methods=['GET'])
def cassava():
    plant = 'cassava'
    session['plant'] = plant
    session['path'] = PATH + 'plant_models/cassava_inception_v3.h5'
    return render_template('cassava.html', title=plant)



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    plant_name = session.get('plant')
    MODEL_PATH = session.get('path')
    model = load_model(MODEL_PATH, custom_objects=None, compile=True)

    print('\n')
    print(MODEL_PATH)
    print('\n')
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = model_predict(file_path, model, plant_name)
        return result


    return None



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)

