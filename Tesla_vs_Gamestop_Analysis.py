from bs4 import BeautifulSoup
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

TSLA = yf.Ticker('TSLA')
TSLA_info = TSLA.info
TSLA_Share_Price_Info = TSLA.history(period='max')
TSLA_Share_Price_Info.reset_index(inplace=True)
print(TSLA_Share_Price_Info)

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
data = requests.get(url).text
soup = BeautifulSoup(data, 'html5lib')

TSLA_Revenue_Data = pd.DataFrame(columns=['Date', 'Revenue'])
for row in soup.find_all('tbody')[1].find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text
    TSLA_Revenue_Data = TSLA_Revenue_Data.append({'Date':date,'Revenue':revenue},ignore_index=True)

TSLA_Revenue_Data["Revenue"] = TSLA_Revenue_Data['Revenue'].str.replace(',|\$',"")
print(TSLA_Revenue_Data.isnull().sum())
TSLA_Revenue_Data.dropna(inplace=True)
TSLA_Revenue_Data = TSLA_Revenue_Data[TSLA_Revenue_Data['Revenue'] != ""]
print(TSLA_Revenue_Data.tail())

GME = yf.Ticker('GME')
GME_info = GME.info
GME_Share_Price_Info = GME.history(period='max')
GME_Share_Price_Info.reset_index(inplace=True)
print(GME_Share_Price_Info)

url2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
data = requests.get(url2).text
soup2 = BeautifulSoup(data, 'html5lib')

GME_Revenue_Data = pd.DataFrame(columns=['Date','Revenue'])
for row in soup2.find_all('tbody')[1].find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text
    GME_Revenue_Data = GME_Revenue_Data.append({'Date':date,'Revenue':revenue},ignore_index=True)
GME_Revenue_Data["Revenue"] = GME_Revenue_Data['Revenue'].str.replace(',|\$',"")
print(GME_Revenue_Data.tail())
make_graph(TSLA_Share_Price_Info,TSLA_Revenue_Data,'Tesla')
make_graph(GME_Share_Price_Info,GME_Revenue_Data,'Gamestop')