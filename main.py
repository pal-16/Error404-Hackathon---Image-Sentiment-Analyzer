import os
import secrets
from PIL import Image
from flask import Flask,session, render_template, url_for,flash,redirect,request
from init import app, db , bcrypt
import os
from sqlalchemy.orm import Session
from flask_bcrypt import (Bcrypt,
                          check_password_hash,
                          generate_password_hash,)
import tensorflow
from forms import RegistrationForm,LoginForm
from models import Org,ImageLink
from flask_login import login_user, current_user, logout_user, login_required

from EmoPy.src.fermodel import FERModel

global graph
graph = tensorflow.get_default_graph() 

target_emotions = ['anger','fear','surprise']
model = FERModel(target_emotions,verbose=True)

import glob
import re
import numpy as np
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import load_img,img_to_array
#from __future__ import division, print_function
# coding=utf-8
#import sys

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# db2 = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///count.db'

# class Count(db2.Model):
#     count:db2.Column(db2.Number,primary_key=True)
# model = load_model("final_model.h5")

def preprocess(image):
    image = img_to_array(image,target_size=(224,224))
    image = np.array(image).astype("float32")
    image = image/255
    image = np.expand_dims(image,axis=0)
    return image



def create_session(config):
    engine = create_engine(config['DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session 
    

@app.route('/add',methods=['GET','POST'])
def add_image():
    return render_template('add_image.html')

@app.route('/addHappyImages',methods=['POST'])
def addImage():
    try:
        image_link = request.form['link']
        print(image_link)
        db.session.add(ImageLink(link=image_link))
        db.session.commit()
        return redirect('/add')
    except:
        print('error')
    
   
@app.route('/flashMessage')
def flas():
   return render_template('flashMessage.html')

@app.route("/")
def main():
    return redirect("/index")

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/alert/happy.html")
def happy():
    images = ImageLink.query.all()
    return render_template('happy.html',images=images)


@app.route("/choose")
def choose():
    return render_template('choose.html')

@app.route("/webcam")
def webcam():
    return render_template('webcam.html')




@app.route("/alert/<int:flag>")
def alert(flag):
    print(flag)
    print(type(flag))
    return render_template('alert.html',flag=flag)

@app.route('/predict2', methods=['GET', 'POST'])
def predict2():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        print(type(file_path))
        f.save(file_path)
        print("hello")
        with graph.as_default():
            result = model.predict(file_path)
        print(result)
        if result=='anger' or result=='fear':
        # # result = model.predict_classes(preprocess(load_img(file_path)))
            return redirect('/alert/0')
        else:
            return redirect('/alert/1')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        print(type(file_path))
        f.save(file_path)
        print("hello")
        with graph.as_default():
            result = model.predict(file_path)
        print(result)
        if result=='anger' or result=='fear':
        # # result = model.predict_classes(preprocess(load_img(file_path)))
            return redirect('/alert/0')
        else:
            return redirect('/alert/1')
        # Get the file from post request
       
        
        # Save the file to ./uploads
        

        # Make prediction
      #  preds = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
       # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        #result = str(pred_class[0][0][1])               # Convert to string
       # return result
    #return None
    return render_template('index.html')
 

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        org =Org.query.filter_by(email=form.email.data,password=form.password.data).first()
        if org:
            login_user(org, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/index')
        else:
            flash('Login Unsuccessful. Please check email and password')
            return redirect(url_for('/'))
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return render_template('logout.html')


      
@app.route("/reg", methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        org= Org(name=form.name.data,email=form.email.data,password=form.password.data)
        print(org)
        db.session.add(org)
        db.session.commit()
        flash('You were successfully signed up')
        return redirect('/index')
        
    return render_template('dec.html', title='decregister', form=form)


