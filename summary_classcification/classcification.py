import os
import json
from difflib import SequenceMatcher

def process_files(directory):
    # 初始化分類結果字典
    classified_texts = {keyword: [] for keyword in keywords}

    # 指定目錄，處理每個檔案
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    if "summary_text" in line:
                        classified = False
                        for keyword in keywords:
                            if keyword in line:
                                classified_texts[keyword].append(line.strip())
                                classified = True
                                break
                        if not classified:
                            most_similar_keyword = max(keywords, key=lambda x: similar(line, x))
                            classified_texts[most_similar_keyword].append(line.strip())

    # 輸出分類結果
    output_json(classified_texts)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def output_json(classified_texts):
    with open('classify.json', 'w', encoding='utf-8') as f:
        json.dump(classified_texts, f, ensure_ascii=False, indent=4)

def main():
    directory = '/Users/xuzhiwei/GDSC-ai-stock/summary_classcification'  # 指定包含檔案的目錄路徑
    process_files(directory)

if __name__ == '__main__':
    keywords = [ 'battery' ,'electric vehicle', 'Power', 'Full Self-Driving', 'Supercharger network', 'Destination charging',
                'location network', 'Insurance services', 'Autopilot', 'North American Charging Standard']
    main()
