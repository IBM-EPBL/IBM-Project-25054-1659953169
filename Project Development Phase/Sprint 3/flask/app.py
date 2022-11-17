from flask import Flask,render_template,request
import pickle
import numpy as np

model=pickle.load(open('kidney.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict_satisfaction():
    name = request.form.get('name')

    v1 = float(request.form.get('sg'))

    v2 = request.form.get('htn')
    v2 = 0 if 'No' else 1

    v3 = float(request.form.get('hemo'))

    v4 = request.form.get('dm')
    v4 = 0 if 'No' else 1

    v5 = int(request.form.get('al'))

    v6 = int(request.form.get('appet'))
    v6 = 0 if 'Poor' else 1

    v7 = float(request.form.get('rc'))

    v8 = request.form.get('pe')
    v8 = 0 if 'Yes' else 1

    #prediction
    result=model.predict(np.array([v1,v2,v3,v4,v5,v6,v7,v8]).reshape(1,8))
    d={0:"Negative",1:"Positive"}
    prediction_result=d[result[0]]
    return render_template('report.html',res=prediction_result,pname=name)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)
