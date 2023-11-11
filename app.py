import os

import numpy as np
import pandas as pd
import pickle
import requests

from flask import Flask, render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r'C:\Users\samuo\PycharmProjects\flask_junction\data\uploads'

app = Flask(__name__)
app.secret_key = 'albos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#model = pickle.load(open('model.pkl','rb'))


latest_upload = '1'

@app.route('/api',methods=['POST'])
def predict():
    #data = request.get_data()
    #data = request.get_json(force=True)
    #data = [5.762711864406779849e-01, 3.576271186440677763e+00, 1.000000000000000000e+00, 2.365040000000000146e+04, 6.001000000000000000e+03, 8.347600000000000364e+03, 1.445460000000000036e+04, 1.411500000000000000e+04, 9.198000000000000000e+03, 2.365040000000000146e+04, 6.001000000000000000e+03, 8.347600000000000364e+03, 1.445460000000000036e+04, 1.411500000000000000e+04, 9.198000000000000000e+03]
    data = [-3.505084745762711673e+00, -4.569491525423728717e+00, 1.000000000000000000e+00, 2.712361542538167214e+02, 1.896659999999999854e+04, 5.229199999999999818e+03, 7.604199999999999818e+03, 9.851000000000000000e+03, 8.948399999999999636e+03, 6.573600000000000364e+03, 1.389660000000000036e+04, 4.429600000000000364e+03, 8.158399999999999636e+03, 8.919200000000000728e+03, 8.721200000000000728e+03, 1.218400000000000000e+04]
    values1 = np.reshape(data, (-1, 16))
    prediction = model.predict(values1)

    #prediction = model.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return str(output)

def pandas(data):
    df = pd.read_json(data)
    df.to_csv('test.csv')
    return pd.read_csv('test.csv').head(1)

def change_last(name):
    global latest_upload
    latest_upload = name

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')
@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      change_last(f.filename)
      flash("File successfully uploaded")
      return redirect("/")



if __name__ == '__main__':
    app.run()
