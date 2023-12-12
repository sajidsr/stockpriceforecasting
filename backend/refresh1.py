from flask import Blueprint, redirect, url_for
from flask_login import LoginManager, login_required

from models import db, Users

refresh = Blueprint('refresh', __name__, template_folder='../Templates')
login_manager = LoginManager()
login_manager.init_app(refresh)

@refresh.route('/refresh', methods=['GET','POST'])
@login_required
def refreshgraph():
    import pandas as pd
    import numpy as np
    import plotly.graph_objs as go
    import plotly.io as pio

    import pandas_datareader as pdr
    key=""

    df = pdr.get_data_tiingo('AAPL', api_key='385c9d752ffbcfbf8e3bbaa5f638acc702c37d68')

    df.to_csv('frontend/static/data/app.csv')
    df=pd.read_csv('frontend/static/data/app.csv')

    # create a Plotly trace for the line chart
    trace = go.Scatter(x=df['date'], y=df['close'])
   ## data = [trace]
    
    # create a Plotly layout for the chart
    layout = go.Layout(title='Stock Price', xaxis=dict(title='date'), yaxis=dict(title='close'))
    
    # create a Plotly figure using the data and layout
    fig = go.Figure(data=[trace], layout=layout)
    pio.write_html(fig, file='frontend/static/graphs/apple_his_graph.html', include_plotlyjs='cdn', auto_play=True)



    

    import tensorflow as tf
    model = tf.keras.models.load_model('frontend/static/model/LSTM.h5')

    df=df['close']

    df=df.tail(100)

    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))
    df1=scaler.fit_transform(np.array(df).reshape(-1,1))

    x_input=df1.reshape(1,-1)

    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()

    #prediction for next 10 days
    from numpy import array

    lst_output=[]
    n_steps=100
    i=0
    while(i<30):
        
        if(len(temp_input)>100):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            ##print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            ##print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            ##print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            ##print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1

    day_new=np.arange(1,101)
    day_pred=np.arange(101,111)

    pred=scaler.inverse_transform(lst_output)
    actual=scaler.inverse_transform(df1)

    import plotly.graph_objs as go
    import plotly.offline as pyo

    pred = np.ravel(pred)
    actual = np.ravel(actual)

    trace1 = go.Scatter(
    x=day_new,
    y=actual,
    mode='lines',
    name = "Last 100 days Stock Price"
    )

    trace2 = go.Scatter(
    x=day_pred,
    y=pred,
    mode='lines',
    name="Next 10 days forecasting",
    line=dict(color='orange')
    )

    layout = go.Layout(
        title='Apple Forecasting Graph', xaxis=dict(title='Number of Days'), yaxis=dict(title='Closing Price')
    )

    fig = go.Figure(data=[trace1,trace2], layout=layout)
    fig1 = go.Figure(data=[trace2], layout=layout)
    pio.write_html(fig1, file='frontend/static/graphs/apple_pred_graph.html', include_plotlyjs='cdn', auto_play=True)
    # ... create the plot ...
    pio.write_html(fig, file='frontend/static/graphs/apple_graph.html', include_plotlyjs='cdn', auto_play=True)
    return redirect(url_for('regraph.show'))
    
