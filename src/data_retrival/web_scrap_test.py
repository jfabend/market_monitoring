import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.macrotrends.net/stocks/charts/XYL/xylem/income-statement?freq=Y'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.findAll('div'))