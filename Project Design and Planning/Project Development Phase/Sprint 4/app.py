from flask import Flask,render_template,request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "53WbjoDkinpv78FeGLOzcscvYlnmhVF4M4vgU5h1rV_1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#model=pickle.load(open('kidney.pkl','rb'))
app=Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
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

    t = [[v1, int(v2), v3, int(v4), v5, int(v6), v7, int(v8)]]
    print(t)
    payload_scoring = {"input_data": [{"field": [["sg", "htn", "hemo", "dm", "al", "appet", "rc", "pe"]], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2482ca43-5c91-4ab8-8959-ec30a7e635f7/predictions?version=2022-11-17', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
    
    predictions = response_scoring.json()
    print(predictions)

    pred = predictions["predictions"][0]["values"][0][0]
    if pred == 0:
        output = "Negative"
    else:
        output = "Positive"
    print(output)
    #return render_template('index.html',prediction_text = output)
    return render_template('report.html',prediction_text = output, your_name = name)

if __name__=='__main__':
    app.run(debug = True)
