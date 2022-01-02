from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
import pickle
import numpy as np
views = Blueprint('views', __name__)


def predict(values):
   # if len(values) == 10:
   print(len(values))
   model = pickle.load(open("chronic.pkl", "rb"))
   values = np.asarray(values)
   print(values)
   return model.predict(values.reshape(1, -1))[0]

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/kidney", methods=['POST','GET'])
@login_required
def kidney():
    return render_template('kidney.html',user=current_user)

@views.route("/predict", methods = ['POST', 'GET'])
#@login_required
def predictPage():
    
    if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            print(to_predict_dict)
            to_predict_list = list(map(float, list(to_predict_dict.values())))
            print(to_predict_list,len(to_predict_list))
            pred = predict(to_predict_list)
    else:
        flash( "Please enter valid Data", category='error')
        return render_template("home.html",user=current_user)
  

    return render_template('predict.html',user=current_user, pred = pred)



