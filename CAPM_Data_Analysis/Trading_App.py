import streamlit as st

st.set_page_config(page_title="Trading App", 
                   page_icon="chart_with_downwards_trend:", 
                   layout='wide')

st.title("Trading Guide App :bar_chart:")

st.header("We provide the Greatest platform for you to collect all information prior to investing in stocks.")

st.image("app.png")

st.markdown("## We provide the following services: ")

st.markdown("### :one: Stock Information")
st.write("Through the page, you can see all the information about stock. ")

st.markdown("### :two: Stock Prediction")
st.write("###You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forcasting models. Use this tool to gain valuable insights into market trends and make informed investment decisions. ")

st.markdown("### :three: CAPM return")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks assest based on its risk and market performance. ")

st.markdown("### :four: CAPM Beta")
st.write("Calculates Beta and Expected return for Individual stocks")