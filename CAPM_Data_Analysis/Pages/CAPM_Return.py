## importing libraries

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta
import datetime
import pandas_datareader.data as web
import pages.utils.capm_function as capm_function

st.set_page_config(page_title="CAPM Return Calculator", page_icon="📈", layout='wide')
st.title("CAPM Return Calculator")

## getting input from user
col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Select 4 stocks to compare",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','GOOGL','NVDA'),['TSLA','AAPL','AMZN','GOOGL'],key='stocks')
with col2:
    year = st.number_input("Enter the number of years to compare", 1, 10, key='years')

## downloading dta for SP500
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
    SP500 = web.DataReader(['sp500'], 'fred', start, end)

    stocks_df = pd.DataFrame()

    for stocks in stocks_list:
        data = yf.download(stocks, period=f'{year}y')
        stocks_df[f'{stocks}'] = data['Close']


    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)

    SP500 = SP500.rename(columns={'DATE': 'Date'})

    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')


    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)


    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the stocks")
        st.plotly_chart(capm_function.interactive_plot(stocks_df))
    with col2:
        st.markdown("### Price of all the stocks after normalizing")
        st.plotly_chart(capm_function.interactive_plot(capm_function.normalize(stocks_df)))

    stocks_daily_return = capm_function.daily_return(stocks_df)
    print(stocks_daily_return.head())

    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b, a = capm_function.calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    print(beta, alpha)

    beta_df = pd.DataFrame(beta.items(), columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    with col1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df, use_container_width=True)

    rf = 0
    rm = stocks_daily_return['sp500'].mean()*252

    return_df = pd.DataFrame()
    return_value = []
    for stocks, value in beta.items():
        return_value.append(str(round(rf + (value*(rf-rm)),2)))
    return_df['Stock'] = stocks_list

    return_df['Return Value'] = return_value

    with col2:
        st.markdown("### Calculated Return using CAPM")
        st.dataframe(return_df, use_container_width=True)

except:
    st.write("Please select a valid stock") 




