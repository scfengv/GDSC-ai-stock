import time
import find_csv
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

title_list = []
date_list = []

my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level = 3")
chrome_options.add_argument(f"--user-agent = {my_user_agent}")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service()
driver = webdriver.Chrome(service = service, options = chrome_options)

url  = "https://www.cnbc.com/search/?query=tsla&qsearchterm=tsla"
driver.get(url)
wait = WebDriverWait(driver, 60)
search_results = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "SearchResults-searchResultsContainer")))

path = "/Users/shenchingfeng/GitHub/GDSC-ai-stock/News_History"
conti = True
output_count = 0
current_count = 0
target_count = 17859

while conti:

    block = driver.find_elements(By.CLASS_NAME, "SearchResult-searchResultContent")

    new_data_found = False

    for n in block:
        try:
            title = n.find_element(By.CLASS_NAME, "Card-title").text
            title = str(title)
            date = n.find_element(By.CLASS_NAME, "SearchResult-publishedDate").text.split(' ')[0]

            if title not in title_list:

                title_list.append(title)
                date_list.append(date)
                current_count += 1

                if current_count % 1000 == 0:

                    df = pd.DataFrame({
                        "Date": date_list,
                        "News Title": title_list
                    })

                    df.to_csv(fr"{path}/News_history_{output_count}.csv", index = False)
                    output_count += 1
                    title_list.clear()
                    date_list.clear()

        except Exception as e:
            print(e)
            continue
    
    result = find_csv(path)
    
    if len(result) >= target_count:
        conti = False

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    print(f"News Num: {current_count}", end = "\r")
    
df = pd.DataFrame({
    "Date": date_list,
    "News Title": title_list
})

df.to_csv(f"News_history_{output_count}.csv", index = False)
driver.quit()