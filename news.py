import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

title_list = []
date_list = []

options = Options()
options.add_argument('--headless')
options.add_argument('window-size = 800x600')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options = options)

url  = "https://www.cnbc.com/search/?query=tsla&qsearchterm=tsla"
driver.get(url)
wait = WebDriverWait(driver, 60)
search_results = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "SearchResults-searchResultsContainer")))

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')


target_count = 100
current_count  = 0

while (current_count < target_count):

    news_div = soup.find("div", id = "searchcontainer").find_all("div")

    for n in news_div:

        try:
            block = n.find("div", class_ = "SearchResult-searchResultContent")

            title = block.find("div", class_ = "SearchResult-searchResultTitle").find("span").text
            title = str(title)
            if title not in title_list:
                title_list.append(title)

                date = block.find("span", class_ = "SearchResult-byline").find("span", class_ = "SearchResult-publishedDate").text
                date = str(date).split(' ')
                date_list.append(date[0])
                current_count += 1

        except:
            continue
    
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

    # print(title_list)
    # print(date_list)

    print(f"News Num: {current_count}")
    
df = pd.DataFrame({
    "Date": date_list,
    "News Title": title_list
})

df.to_csv("News_history.csv", index = False)
driver.quit()