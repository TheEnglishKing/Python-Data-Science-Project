#import the necessary packages
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

#make_graph provided by the assignment
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
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Question 1: Use yfinance to extract tesla stock data
Tesla = yf.Ticker('TSLA')
tesla_data = Tesla.history(period='max')
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Question2: use webscraping to rxtract telsa revenue data
# get request
url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data = requests.get(url).text
print(html_data)

#parse the html code
soup_data = BeautifulSoup(html_data, 'html5lib')
tesla_dataframe = pd.DataFrame(columns=['Date', 'Revenue'])

#extract the table
for row in soup_data.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    # Finally we append the data of each row to the table
    tesla_dataframe = tesla_dataframe._append({"Date":date, "Revenue":revenue}, ignore_index=True)

#reformat the data
print(tesla_dataframe)
tesla_dataframe['Revenue'] = tesla_dataframe['Revenue'].str.replace('$','')
tesla_dataframe['Revenue'] = tesla_dataframe['Revenue'].str.replace(',','')
tesla_dataframe
tesla_dataframe.tail()

#Question 3: use yfinance to extrack gme data
gamestop = yf.Ticker('GME')
gme_data = gamestop.history(period='max')
gme_data.reset_index(inplace=True)
gme_data.head()

#Question 4: use webscraping to extract GME revenue data
url2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data_gme = requests.get(url2).text

#parse the html code
soup_data2 = BeautifulSoup(html_data_gme, 'html5lib')
gme_dataframe = pd.DataFrame(columns=['Date', 'Revenue'])

#extract the table
for row in soup_data2.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    # Finally we append the data of each row to the table
    gme_dataframe = gme_dataframe._append({"Date":date, "Revenue":revenue}, ignore_index=True)

#reformat the gme code
gme_dataframe
gme_dataframe['Revenue'] = gme_dataframe['Revenue'].str.replace('$','')
gme_dataframe['Revenue'] = gme_dataframe['Revenue'].str.replace(',','')
gme_dataframe
gme_dataframe.tail()

#Question 5: plot tesla stock graph
make_graph(tesla_data, tesla_dataframe, 'Tesla')

#Question 6: plot gme stock graph
make_graph(gme_data, gme_dataframe, 'GameStop')

