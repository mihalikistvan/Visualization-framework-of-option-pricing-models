from flask import Flask,render_template, request
import os
from functions.testCalculation import predictFunc
from yahoo_fin import options


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
    model = request.args.get("modelID","")
    
    
    if predictionType =="ticker":
        responseMessage =""
        tickerNumber = request.args.get("tickerNumber","")
        option = options.get_options_chain(tickerNumber)
        print (option)
        
        bidPrice = request.args.get("bidPrice",0)
        askPrice = request.args.get("askPrice",0)
        strikePrice = request.args.get("strikePrice",1)
        expiration = request.args.get("expiration","2020-12-12")
        quoteDatetime = request.args.get("quoteDatetime","2020-12-11")
        underlying_bid = request.args.get("underlying_bid",0)
        underlying_ask = request.args.get("underlying_ask",1)
        moneyness = float(underlying_ask)/float(strikePrice)
        
        prediction = predictFunc(bidPrice,askPrice,expiration,quoteDatetime,strikePrice,moneyness,underlying_bid,underlying_ask,model)
        
        return render_template("calculation.html",responseMessage=responseMessage, tickerNumber = tickerNumber,predictionType= predictionType, option=option, prediction=prediction)
    
    if predictionType =="manual":
        responseMessage=""
        bidPrice = request.args.get("bidPrice","")
        askPrice = request.args.get("askPrice","")
        strikePrice = request.args.get("strikePrice","")
        expiration = request.args.get("expiration","")
        quoteDatetime = request.args.get("quoteDatetime","")
        underlying_bid = request.args.get("underlying_bid","")
        underlying_ask = request.args.get("underlying_ask","")
        moneyness = float(underlying_ask)/float(strikePrice)

        prediction = predictFunc(bidPrice,askPrice,expiration,quoteDatetime,strikePrice,moneyness,underlying_bid,underlying_ask,model)
       
        return render_template("calculation.html",predictionType=predictionType, responseMessage=responseMessage,bidPrice = bidPrice,
                                askPrice= askPrice, moneyness= moneyness, strikePrice=strikePrice, expiration= expiration,quoteDatetime= quoteDatetime,prediction=prediction)
    else:
        return render_template("calculation.html",responseMessage="No data given to predict with")
@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
