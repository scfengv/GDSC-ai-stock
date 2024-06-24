import time
import pandas as pd

import concurrent.futures
from utils import find_csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

date_list = []
title_list = []

def process_block(block):
    result = []
    for n in block:
        try:
            title = n.find_element(By.CLASS_NAME, "Card-title").text
            title = str(title)

            date_str = n.find_element(By.CLASS_NAME, "SearchResult-publishedDate").text.split(' ')[0]
            date = datetime.strptime(date_str, '%m/%d/%Y')
            result.append((title, date))

        except Exception as e:
            print(e)
            continue

    return result

def main():
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level = 3")
    chrome_options.add_argument(f"--user-agent = {my_user_agent}")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://www.cnbc.com/search/?query=tsla&qsearchterm=tsla"
    driver.get(url)
    wait = WebDriverWait(driver, 60)
    search_results = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "SearchResults-searchResultsContainer")))

    path = "/Users/shenchingfeng/GitHub/GDSC-ai-stock/News_History"
    result = find_csv(path)
    all_title = list(result["News Title"])
    conti = True
    output_count = 0
    current_count = len(all_title)
    target_count = 17870

    newest = driver.find_element(By.ID, "sortdate").click()

    while current_count < target_count:
        block = driver.find_elements(By.CLASS_NAME, "SearchResult-searchResultContent")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_block, [block[i:i+100] for i in range(0, len(block), 100)])

        for title_date_pairs in results:
            for title, date in title_date_pairs:

                if date.year < 2020:
                    break

                if title not in all_title:

                    all_title.append(title)
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
                
                else:
                    print(date, end = "\r")

        if len(all_title) >= target_count:
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "SearchResults-searchResultsContainer")))
        print(f"News Num: {current_count}", end = "\r")

    df = pd.DataFrame({
        "Date": date_list, 
        "News Title": title_list
    })
    
    df.to_csv(f"News_history_{output_count}.csv", index = False)
    driver.quit()

if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f"Total time: {end_time - start_time}")