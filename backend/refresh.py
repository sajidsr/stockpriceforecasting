from flask import Blueprint, redirect, request, url_for
from flask_login import LoginManager, login_required

from models import db, Users

refresh = Blueprint('refresh', __name__, template_folder='../Templates')
login_manager = LoginManager()
login_manager.init_app(refresh)

@refresh.route('/refresh', methods=['POST'])
@login_required
def refreshgraph():
    import pandas as pd
    import numpy as np
    import plotly.graph_objs as go
    import plotly.io as pio

    import pandas_datareader as pdr
    key=""

    df = pdr.get_data_tiingo('AAPL', api_key='385c9d752ffbcfbf8e3bbaa5f638acc702c37d68')

    df.to_csv('../frontend/static/data/app.csv')
    df=pd.read_csv('../frontend/static/data/app.csv')

    # create a Plotly trace for the line chart
    trace = go.Scatter(x=df['date'], y=df['close'])
   ## data = [trace]
    
    # create a Plotly layout for the chart
    layout = go.Layout(title='Stock Price', xaxis=dict(title='date'), yaxis=dict(title='close'))
    
    # create a Plotly figure using the data and layout
    fig = go.Figure(data=[trace], layout=layout)
    pio.write_html(fig, file='../frontend/static/graphs/apple_his_graph.html', include_plotlyjs='cdn', auto_play=True)



    

    import tensorflow as tf
    model = tf.keras.models.load_model('../frontend/static/model/Apple_Mul_1_LSTM.h5')

    

    from sklearn.preprocessing import MinMaxScaler
    import tensorflow as tf


    pandemic = int(request.form['name'])
    #pandemic=0
    # Add a new column with all 1s
    df['pandemic'] = 0

    # Scale the 'Close' and 'new_column' columns
    scaler = MinMaxScaler(feature_range=(0, 1))
    df[['close', 'pandemic']] = scaler.fit_transform(df[['close', 'pandemic']])

    # Get the last 100 days of data
    df = df.tail(100)

    # Prepare the input for prediction
    df1 = df[['close', 'pandemic']]
    df1 = np.array(df1).reshape(1, -1)



    df_input = df1.reshape(1, -1)


    # Perform prediction for the next 30 days
    temp_input=list(df_input)
    temp_input=temp_input[0].tolist()


    n_steps = 100
    lst_output = []
    temp_input = list(df_input[0])


    for i in range(30):
        if len(temp_input) > n_steps * 2:
            x_input = np.array(temp_input[-n_steps*2:])
            x_input = x_input.reshape(1, n_steps, 2)
            #print('input2')
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print('output2')
            #print(yhat)
            temp_input.extend(yhat[0].tolist())
            temp_input.append(pandemic)
            temp_input = temp_input[2:]
            #print('temp')
            #(temp_input)
            lst_output.append(yhat.tolist())
            i=i+1
        else:
            x_input = df_input.reshape((1, n_steps, 2))
            #print('input1')
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print('output1')
            #print(yhat)
            temp_input.extend(yhat[0].tolist())
            temp_input.append(pandemic)
            #print('temp')
            #print(temp_input)
            lst_output.append(yhat.tolist())
            i=i+1


    # Extract only the predicted values and reshape them
    pred = np.array(lst_output)
    #Get only the 'Close' column of the predicted values
    pred = pred[:, 0]




    # Extract only the predicted values and reshape them
    pred = np.array(lst_output).reshape(-1, 1)

    # Create a dummy column with zeros
    dummy_column = np.zeros_like(pred)

    # Concatenate the predicted values with the dummy column
    pred = np.concatenate((pred, dummy_column), axis=1)

    # Inverse transform the predicted and actual values
    pred = scaler.inverse_transform(pred)
    actual = scaler.inverse_transform(df[['close', 'pandemic']])

    # Get only the 'Close' column of the predicted values
    pred = pred[:, 0]

    # Flatten the arrays
    actual = actual[:, 0].ravel()

    # Create the plot
    day_new = np.arange(1, 101)
    day_pred = np.arange(101, 131)

    trace1 = go.Scatter(
        x=day_new,
        y=actual,
        mode='lines',
        name="Last 100 days Stock Price"
    )

    trace2 = go.Scatter(
        x=day_pred,
        y=pred,
        mode='lines',
        name="Next 30 days forecasting",
        line=dict(color='orange')
    )

    layout = go.Layout(
        title='30 days forecasting',
        xaxis=dict(title='Number of days'),
        yaxis=dict(title='Closing Stock Price')
    )

    #fig = go.Figure(data=[trace1, trace2], layout=layout)
    
    #fig.write_html('forecasting_plot_final4.html')





    # Save the plot as an HTML file
    fig = go.Figure(data=[trace1,trace2], layout=layout)
    fig1 = go.Figure(data=[trace2], layout=layout)
    pio.write_html(fig1, file='../frontend/static/graphs/apple_pred_graph.html', include_plotlyjs='cdn', auto_play=True)
    # ... create the plot ...
    pio.write_html(fig, file='../frontend/static/graphs/apple_graph.html', include_plotlyjs='cdn', auto_play=True)
    return redirect(url_for('regraph.show'))
    
