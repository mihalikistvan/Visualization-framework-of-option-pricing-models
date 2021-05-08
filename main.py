from flask import Flask,render_template, request
import os
from functions.testCalculation import predictFunc,blackScholes
from yahoo_fin import options
import numpy as np
import pandas
import matplotlib.pyplot as plt


templateDirectory = os.path.abspath('./htmlTemplates')

app = Flask(__name__,template_folder=templateDirectory)


@app.route('/')
def index():

    return render_template("index.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/calculation', methods=['GET', 'POST'])
def calculation():
    predictionType = request.args.get("predictionType","")
    model = request.args.get("type","")
    
    if predictionType =="manual":
        responseMessage=""
        bidPrice = float(request.args.get("bidPrice",""))
        askPrice = float(request.args.get("askPrice",""))
        strikePrice = float(request.args.get("strikePrice",""))
        expiration = request.args.get("expiration","")
        quoteDatetime = request.args.get("quoteDatetime","")
        sp500 = float(request.args.get("sp500",""))
        vix = float(request.args.get("vix",""))
        riskFree = float(request.args.get("riskFree",""))
        moneyness = float(sp500)/float(strikePrice)
        volatility = float(request.args.get("volatility",""))

        prediction = predictFunc(bidPrice,askPrice,expiration,quoteDatetime,strikePrice,moneyness,sp500,vix,riskFree,model)
        plt.plot(prediction)   
        try:
            plt.savefig('static/images/new_plot.png')
        except:
            pass
        bs = blackScholes(sp500, strikePrice, quoteDatetime,expiration, riskFree, volatility, model)
        print ("BS",bs)
        print (prediction[-1])
        return render_template("calculation.html",predictionType=predictionType, responseMessage=responseMessage,bidPrice = bidPrice,
                                askPrice= askPrice, moneyness= moneyness, strikePrice=strikePrice, expiration= expiration,quoteDatetime= quoteDatetime,prediction=prediction[-1],
                                 url='/static/images/new_plot.png', bs=bs)
    else:
        return render_template("calculation.html",responseMessage="No data given to predict with")
@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
