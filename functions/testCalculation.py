from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn.preprocessing import MinMaxScaler
import scipy.stats as si
import sympy as sy
from sympy.stats import cdf

def predictFunc(bidPrice,askPrice,expiration,quoteDatetime,strikePrice,moneyness,sp500,vix,riskFree,model):
    
    timeToMat = (datetime.datetime.strptime(expiration, '%Y-%m-%d')-datetime.datetime.strptime(quoteDatetime, '%Y-%m-%d')).days
    
    returnList=[]
    
    scaler = MinMaxScaler(feature_range=(0,1))
    notScaledBigDataframe = pd.read_csv('toScale.csv')
    for day in range(timeToMat,0,-1):
        
        toPredict = pd.DataFrame(data={}, index=[0])
        toPredict["currentBid"]=float(bidPrice)
        toPredict["currentAsk"]=float(askPrice)
        toPredict["expiration"]=float(day)
        toPredict["strike"]=float(strikePrice)
        toPredict["moneyness"]=float(moneyness)
        toPredict["vixIndex"]=float(vix)
        toPredict["sp500UnderlyingSpot"]=float(sp500)
        toPredict["riskFree"]=float(riskFree)

        if model == 'callModell':
            toPredict["type"]=0.0
        else:
            toPredict["type"]=1.0

        notScaledBigDataframe = notScaledBigDataframe.append(toPredict,ignore_index=True)
        
    del notScaledBigDataframe['endingAsk']
    del notScaledBigDataframe['endingBid']
    del notScaledBigDataframe['blackScholes']        

    toPredictScale = scaler.fit_transform(notScaledBigDataframe)
    toPredict = pd.DataFrame(toPredictScale,columns=notScaledBigDataframe.columns.values)

    model = keras.models.load_model(str(model))
    prediction = model.predict(toPredict)
    
    for i in range(len(notScaledBigDataframe)-timeToMat+1,len(notScaledBigDataframe)):
        returnList.append( prediction[i-1][0])
    
    return (returnList)



def blackScholes(sp500, strike, quoteDatetime,expiration, riskFree, volatility, model):
    
    
    expiration=float((datetime.datetime.strptime(expiration, '%Y-%m-%d')-datetime.datetime.strptime(quoteDatetime, '%Y-%m-%d')).days)

    d1 = (np.log(sp500 / strike) + (expiration + 0.5 * volatility ** 2) * expiration) / (volatility * np.sqrt(expiration))
    d2 = (np.log(sp500 / strike) + (expiration - 0.5 * volatility ** 2) * expiration) / (volatility * np.sqrt(expiration))
    
    if model == 'callModell':
        bs = (sp500 * si.norm.cdf(d1, 0.0, 1.0) - strike * np.exp(-riskFree * expiration) * si.norm.cdf(d2, 0.0, 1.0))
    if model == 'putModell':
        bs = (strike * np.exp(-riskFree * expiration) * si.norm.cdf(-d2, 0.0, 1.0) - sp500 * si.norm.cdf(-d1, 0.0, 1.0))
    
    return (bs)
        