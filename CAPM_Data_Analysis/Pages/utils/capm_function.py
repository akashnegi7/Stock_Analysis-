import plotly.express as px
import numpy as np

## function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line(title='Live Bitcoin Price')
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(width = 750, margin = dict(l=20, r=20, t=50, b=20), legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.02, xanchor = 'right', x=1, )) 
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Price')
    return fig

## function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df

## function to calculate daily return
def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            df_daily_return[i][j] = ((df[i][j]-df[i][j-1])/df[i][j-1])*100
        df_daily_return[i][0] = 0
    return df_daily_return

## function to calculate beta
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean()*252

    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a

