import json
import requests

API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

input_file = "2018Q1_split.json"
output_file = "2018Q1_semtiment.json"

with open(input_file, "r") as file:
    data = json.load(file)

output_data = []

for item in data:
    
    for key, value in item.items():
        if key.startswith("paragraph"):
            paragraph_text = value
    
            # 使用 API 處理段落
            result = query({"inputs": paragraph_text})
            print(result)

            sentiment_score = result[0]["summery_text"]  
        
            # 將結果添加到新的資料結構中，包括編號和內容
            output_data.append({ "summary_text": summary_text, "sentiment_score": sentiment_score})

with open(output_file, "w") as file:
    json.dump(output_data, file, indent=4)

print("finish", output_file) 