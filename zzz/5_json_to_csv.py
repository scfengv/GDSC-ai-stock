import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 確定 CSV 文件的列標題
    fieldnames = ['original_text','summary','negative','neutral','positive']

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # 寫入列標題
        writer.writeheader()

        # 寫入每一行數據
        for item in data:
            row = {
                'original_text': item['original_text'],
                'summary': item['summary'],
                'negative': item['sentiment']['negative'],
                'neutral': item['sentiment']['neutral'],
                'positive': item['sentiment']['positive']
            
            }
            writer.writerow(row)

# 設置 JSON 文件路徑和輸出 CSV 文件路徑
json_file = "2014Q4sentiment.json"
csv_file = "2014Q4sentiment.csv"


# 將 JSON 數據轉換為 CSV
json_to_csv(json_file, csv_file)

print("finish")