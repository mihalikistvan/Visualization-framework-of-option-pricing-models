from flask import Flask,render_template, request
import os
from functions.testCalculation import testCalculation
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

model = keras.models.load_model('modelForFlask')
templateDirectory = os.path.abspath('./htmlTemplates')

app = Flask(__name__,template_folder=templateDirectory)

@app.route('/')
def index():
    scale_test = pd.read_csv("predData.csv")
    del scale_test['ending_ask']
    prediction = model.predict(scale_test)
    print (prediction)
    prediction = prediction[0][0]
    return render_template("index.html", prediction=prediction)

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/calculation', methods=['GET', 'POST'])
def calculation():
    
    predictionType = request.args.get("predictionType","")
    
    if predictionType =="ticker":
        responseMessage = testCalculation()
        tickerNumber = request.args.get("tickerNumber","")
        return render_template("calculation.html",responseMessage=responseMessage, tickerNumber = tickerNumber,predictionType= predictionType)
    if predictionType =="manual":
        responseMessage = testCalculation()
        volatility = request.args.get("volatility","")
        bidPrice = request.args.get("bidPrice","")
        askPrice = request.args.get("askPrice","")
        riskFreeRate = request.args.get("riskFreeRate","")
        strikePrice = request.args.get("strikePrice","")
        expiration = request.args.get("expiration","")
        quoteDatetime = request.args.get("quoteDatetime","")

        return render_template("calculation.html",predictionType=predictionType, responseMessage=responseMessage,volatility = volatility,bidPrice = bidPrice,
                                askPrice= askPrice, riskFreeRate= riskFreeRate, strikePrice=strikePrice, expiration= expiration,quoteDatetime= quoteDatetime)
    else:
        return render_template("calculation.html",responseMessage="No data given to predict with")
@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
