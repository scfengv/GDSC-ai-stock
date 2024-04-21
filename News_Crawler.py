import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
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

url = fr"https://finance.yahoo.com/quote/TSLA/news"
driver.get(url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

title_list = []

news_div = soup.find("div", class_ = "filtered-stories x-large svelte-7rcxn rulesBetween infiniteScroll").find_all("li", class_ = "stream-item svelte-7rcxn")

for i in range(len(news_div)):

    ## "Cf" 下面有兩種 Class_
    try: 
        title = news_div[i].find("h3", class_ = "clamp svelte-13zydns").text
    except:
        continue
    title = str(title)
    title_list.append(title)

driver.quit()

# CNBC

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
    
driver.quit()

title_list = list(dict.fromkeys(title_list))

df = pd.DataFrame({
    "Date": datetime.now().strftime('%Y-%m-%d'),
    "News_Title": title_list
})

df.to_csv(f"News_History/News_Title_{datetime.now().strftime('%Y-%m-%d')}.csv")