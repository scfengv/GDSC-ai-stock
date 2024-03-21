from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## Yahoo Finance

options = Options()
options.add_argument('--headless')
options.add_argument('window-size = 800x600')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options = options)

url = fr"https://finance.yahoo.com/quote/TSLA?.tsrc=fin-srch"
driver.get(url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

title_list = []

news_div = soup.find("div", id = "quoteNewsStream-0-Stream", class_ = "tdv2-applet-stream Bdc(#e2e2e6) Pos(r) Z(1)").find("ul", class_ = "My(0) P(0) Wow(bw) Ov(h)").find_all("li", class_ = "js-stream-content Pos(r)")

for i in range(len(news_div)):

    ## "Cf" 下面有兩種 Class_
    try: 
        title = news_div[i].find("div", class_ = "Py(14px) Pos(r)").find("div", class_ = "Cf").find("div", class_ =  ("Ov(h) Pend(44px) Pstart(25px)")).find("h3", class_ = "Mb(5px)").find("a").text
    except:
        title = news_div[i].find("div", class_ = "Py(14px) Pos(r)").find("div", class_ = "Cf").find("div", class_ =  ("Ov(h) Pend(14%) Pend(44px)--sm1024")).find("h3", class_ = "Mb(5px)").find("a").text
    title = str(title)
    title_list.append(title)

driver.quit()

## CNBC

options = Options()
options.add_argument('--headless')
options.add_argument('window-size = 800x600')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options = options)

url = fr"https://www.cnbc.com/search/?query=tesla&qsearchterm=tesla"
driver.get(url)
wait = WebDriverWait(driver, 60)
search_results = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "SearchResults-searchResultsContainer")))

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

news_div = soup.find("div", class_="SearchResults-searchResultsContainer").find("div", id = "searchcontainer").find_all("div")

for i in range(len(news_div)):
    try:
        title = news_div[i].find("div", class_ = "SearchResult-searchResultTitle").find("a").find("span").text
        title = str(title)
        title_list.append(title)
    except:
        continue
    
title_list = list(dict.fromkeys(title_list))

driver.quit()

print(title_list)