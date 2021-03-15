from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn.preprocessing import MinMaxScaler


def predictFunc(bidPrice,askPrice,expiration,quoteDatetime,strikePrice,moneyness,underlying_bid,underlying_ask,model):
    
    toPredict = pd.DataFrame(data={}, index=[0])
    toPredict["bid"]=float(bidPrice)
    toPredict["ask"]=float(askPrice)

    toPredict["timeToMaturity"]=float((datetime.datetime.strptime(expiration, '%Y-%m-%d')-datetime.datetime.strptime(quoteDatetime, '%Y-%m-%d')).days)
    toPredict["strike"]=float(strikePrice)
    toPredict["moneyness"]=float(moneyness)
    toPredict["underlying_bid"]=float(underlying_bid)
    toPredict["underlying_ask"]=float(underlying_ask)
    
    data = {"sP500AdjClose": 2724.8701170000004,"sP500High":2724.98999,"sP500Low":2698.75,"sP500Close":2724.8701170000004, "statisticalVolatility":0.12496959699999999,"vixIndex":15.73,"extremeVolatility":0.045924,"garmanKlass":0.04021257,"riskFree":2.37}
    data =pd.DataFrame(data=data,index=[0])
    toPredict.append(data,ignore_index=True)
    toPredict = pd.concat([toPredict, data], axis=1)
    scaler = MinMaxScaler(feature_range=(0,1))
    toPredictScale = scaler.fit_transform(toPredict)
    toPredict = pd.DataFrame(toPredictScale,columns=toPredict.columns.values)
    
    #ToDo: fix Scaling
    
    print (toPredict)
    model = keras.models.load_model(model)
    
    prediction = model.predict(toPredict)
    
    return prediction[0][0]
