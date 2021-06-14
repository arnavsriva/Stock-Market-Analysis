from flask import Flask,render_template,request
import pandas as pd
#data
from data import *
#models
from lstm_model import *
from arima_model import *
from linearregression_model import *

app = Flask(__name__)
#key for alpha vantage
api_key = 'NY59PBPMWLPHBD8R'

@app.route("/",methods = ["GET","POST"])
def home():
    return render_template("index.html")

@app.route("/predict",methods = ["GET","POST"])
def analysis():
    ticker = request.form['ticker']#getting name of stock    
    try:
        stock_data(ticker)
    except:
        return render_template('index.html',not_found=True)
    else:#preprocessing data to train model
        df = pd.read_csv(''+ticker+'.csv')
        today_stock=df.iloc[-1:]
        df = df.dropna()
        code_list=[]
        for i in range(0,len(df)):
            code_list.append(ticker)
        df2=pd.DataFrame(code_list,columns=['Code'])
        df2 = pd.concat([df2, df], axis=1)
        df=df2


        arima_pred, error_arima=ARIMA_ALGO(df)
        lstm_pred, error_lstm=LSTM_ALGO(df)
        df, lr_pred, forecast_set,mean,error_lr=LIN_REG_ALGO(df)

        today_stock=today_stock.round(2)
        return render_template('results.html',ticker=ticker,arima_pred=round(arima_pred,2),lr_pred=round(lr_pred,2),lstm_pred=round(lstm_pred,2),error_lr=round(error_lr,2),error_lstm=round(error_lstm,2),error_arima=round(error_arima,2))
if __name__=="__main__":
    app.run(debug=True)
