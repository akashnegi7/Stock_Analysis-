import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime

def plotly_table(dataframe):
    rowEvenColor = '#f8fafd'
    rowoddColor = '#e8f0f8'
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>"] + [str(i)  for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=30),
            height=60
        ),
        cells=dict(
            values=[["<b>" + str(i) + "<b>" for i in dataframe.index]] + [dataframe[i] for i in dataframe.columns],
            line_color=["White"],
            fill_color=[[rowoddColor, rowEvenColor] * len(dataframe)],
            align='left',
            font=dict(color=["black"], size=15)
        )
    )])
    return fig

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1) 
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6) 
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1) 
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5) 
    elif num_period == 'ytd':
        date = datetime.datetimr(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                         mode='lines',
                          name='open', line=dict(width=2,color='#5ab7ff')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                         mode='lines',
                          name='close', line=dict(width=2,color='black')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                         mode='lines',
                          name='High', line=dict(width=2,color='#0078ff')))
        fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                         mode='lines',
                          name='Low', line=dict(width=2,color='red')))
        fig.update_xaxes(rangeslider_visible=True)
    
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                 open=dataframe['Open'], high=dataframe['High'], 
                 low=dataframe['Low'], close=dataframe['Close'], name='candlestick'))
   
    return fig


def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], 
        y=dataframe.RSI,
        name='RSI', line=dict(width=2, color='orange'),marker_color='orange'))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70]*len(dataframe),
        name='Overbought', line=dict(width=2, color='red', dash='dash'),marker_color='red'))
    
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30]*len(dataframe),fill='tonexty',
        name='oversold', line=dict(width=2, color='green', dash='dash'),marker_color='green'))

    return fig




def Moving_average(dataframe, num_period):
    dataframe['SMA 50'] = pta.sma(dataframe['Close'],50)
    dataframe = filter_data(dataframe, num_period)
    fig = go. Figure()

    fig.add_trace(go.Scatter (x=dataframe['Date'], y=dataframe ['Open'],
                            mode='lines',
                            name='Open', line = dict( width=2, color = '#5ab7ff')))
    fig.add_trace(go. Scatter (x=dataframe['Date'], y=dataframe ['Close'],
                            mode='lines',
                            name='Close', line = dict( width=2, color = 'black')))
    fig.add_trace(go. Scatter (x=dataframe['Date'], y=dataframe['High'],
                            mode='lines', name='High', line = dict( width=2, color = '#0078ff')))
    fig.add_trace(go. Scatter (x=dataframe ['Date'], y=dataframe ['Low'],
                            mode='lines', name='Low', line = dict( width=2, color = 'red')))
    fig.add_trace(go. Scatter (x=dataframe ['Date'], y=dataframe['SMA_50'],
                            mode='lines', name='SMA_50', line = dict( width=2, color = 'purple')))
    
    fig.update_xaxes (rangeslider_visible=True)

    return fig

def MACD (dataframe, num_period):
    macd=pta.macd(dataframe ['Close']).iloc[:,0]
    macd_signal = pta.macd(dataframe ['Close']).iloc[:,1]
    macd_hist=pta.macd(dataframe ['Close']).iloc[:,2]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe= filter_data(dataframe, num_period)
    fig= go.Figure()
    fig.add_trace(go. Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'], name='RSI', marker_color='orange', line = dict( width=2, color = 'orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'], name = 'Overbought', marker_color='red', line = dict( width=2, color = 'red',dash='dash'),
    ))
    c = ['red' if cl <0 else "green" for cl in macd_hist]
    

    return fig


def moving_average_forecast(forecast):
    fig = go.Figure()

    fig.add_trace(go.scatter(x=forecast.index[:-30],y=forecast['Close'].iloc[:-30],
                             mode = 'lines',
                             name = 'Close Price', line = dict(width=2,color='black')))
    fig.add_trace(go.scatter(x=forecast.index[-31:],y=forecast['Close'].iloc[-31:],
                             mode='lines',name='future close price',line=dict(width=2,color='red')))
    

    fig.update_xaxes(rangeslider_visible=True)

    return fig




