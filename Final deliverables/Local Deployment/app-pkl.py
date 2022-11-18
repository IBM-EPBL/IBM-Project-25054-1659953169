from flask import Flask,render_template,request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

model=pickle.load(open('kidney.pkl','rb'))
app=Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    name = request.form['name']

    v1 = float(request.form['sg'])

    v2 = request.form['htn']
    if(v2 == 'No'):
        v2 = 0
    if v2 == 'Yes':
        v2 = 1

    v3 = float(request.form['hemo'])

    v4 = request.form['dm']
    if(v4 == 'No'):
        v4 = 0
    if v4 == 'Yes':
        v4 = 1

    v5 = int(request.form['al'])

    v6 = request.form['appet']
    if(v6 == 'Poor'):
        v6 = 0
    if v6 == 'Good':
        v6 = 1

    v7 = float(request.form['rc'])

    v8 = request.form['pe']
    if(v8 == 'No'):
        v8 = 0
    if v8 == 'Yes':
        v8 = 1

    result=model.predict(np.array([v1,v2,v3,v4,v5,v6,v7,v8]).reshape(1,8))
    d = {0:"Negative",1:"Positive"}
    output = d[result[0]]
    return render_template('report.html',prediction_text = output, your_name = name)

if __name__=='__main__':
    app.run(debug = True)
