import re
import time
import requests
import selenium
import warnings
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from sympy import symbols, solve
from plotly.subplots import make_subplots
from pandas_datareader import data as pdr
from selenium.webdriver.common.by import By
from forex_python.converter import CurrencyRates
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

warnings.filterwarnings("ignore")

ticker = "TSLA"

##### Profit Ratio

options = Options()
options.add_argument('--headless')
options.add_argument('window-size = 800x600')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options = options)

url = fr"https://stockanalysis.com/stocks/tsla/financials/?p=quarterly"
driver.get(url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

## Date
date_all = []
date_parent = soup.find('th', string = "Quarter Ended").find_all_next('th')
for date in date_parent[:-1]:
    date_all.append(date.text)

## EPS
eps_all = []
eps_parent = soup.find('span', string = "EPS (Diluted)").find_parent('td').find_all_next('td')
for eps in eps_parent[:len(date_all)]:
    eps_all.append(float(eps.text))

## Gross Margin // Gross Profit = Revenue - Cost of Revenue
gross_margin_all = []    
gross_margin_parent = soup.find('span', string = "Gross Margin").find_parent('td').find_all_next('td')
for gross_margin in gross_margin_parent[:len(date_all)]:
    gross_margin_all.append(float(re.sub("%", "", gross_margin.text)))

## Operating Margin // Operating Profit = Revenue - Cost of Revenue - Operating Expenses
opt_margin_all = []
opt_margin_parent = soup.find('span', string = "Operating Margin").find_parent('td').find_all_next('td')
for opt_margin in opt_margin_parent[:len(date_all)]:
    opt_margin_all.append(float(re.sub("%", "", opt_margin.text)))

driver.quit()



##### Solvency ratio

options = Options()
options.add_argument('--headless')
options.add_argument('window-size = 800x600')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options = options)

url = fr"https://stockanalysis.com/stocks/tsla/financials/ratios/?p=quarterly"
driver.get(url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

## Quick Ratio
quick_all = []
quick_parent = soup.find('span', string = "Quick Ratio").find_parent('td').find_all_next('td')
for quick in quick_parent[1:len(date_all)+1]:
    quick_all.append(quick.text)

driver.quit()


df = pd.DataFrame(list(zip(date_all, eps_all , gross_margin_all, opt_margin_all, quick_all)), 
                  columns = ['Date', 'EPS', 'Gross Margin (%)', 'Operating Margin (%)', 'Quick Ratio (%)']
                  )

df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by = ['Date'], ignore_index = True, inplace = True)

df['EPS Growth (YoY%)'] = 0.0
for i in range(len(df)):

    if df['EPS'].iloc[i] > df['EPS'].iloc[i - 4] and df['EPS'].iloc[i - 4] > 0:
        df.loc[df.index[i], 'EPS Growth (YoY%)'] =  round(((df['EPS'].iloc[i] - df['EPS'].iloc[i - 4]) / df['EPS'].iloc[i - 4]) * 100, 2)

    elif df['EPS'].iloc[i] > df['EPS'].iloc[i - 4] and df['EPS'].iloc[i - 4] < 0:
        df.loc[df.index[i], 'EPS Growth (YoY%)'] =  round(((df['EPS'].iloc[i] - df['EPS'].iloc[i - 4]) / df['EPS'].iloc[i - 4]) * 100, 2) * -1

    elif df['EPS'].iloc[i] < df['EPS'].iloc[i - 4] and df['EPS'].iloc[i - 4] > 0:
        df.loc[df.index[i], 'EPS Growth (YoY%)'] =  round(((df['EPS'].iloc[i] - df['EPS'].iloc[i - 4]) / df['EPS'].iloc[i - 4]) * 100, 2)

    elif df['EPS'].iloc[i] < df['EPS'].iloc[i - 4] and df['EPS'].iloc[i - 4] < 0:
        df.loc[df.index[i], 'EPS Growth (YoY%)'] =  round(((df['EPS'].iloc[i] - df['EPS'].iloc[i - 4]) / df['EPS'].iloc[i - 4]) * 100, 2) * -1
        
df['EPS Growth (YoY%)'][0] = 0
df['EPS Growth (YoY%)'][1] = 0
df['EPS Growth (YoY%)'][2] = 0
df['EPS Growth (YoY%)'][3] = 0

df.set_index('Date', inplace = True)
df.to_csv('Financial Statement.csv')