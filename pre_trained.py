import json
import os
import requests
from tqdm import tqdm

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": "Bearer APIKEY"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


data_folder = "Data"
for filename in tqdm(os.listdir(data_folder), desc="Total file"):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        with open(file_path, "r") as file:
            data = json.load(file)

        for tweet_id, tweet_info in tqdm(data.items(), desc="Current file processing"):
            tweet_text = tweet_info["text"]
            output = query({"inputs": tweet_text})
            # 創建情感分析結果的字典
            sentiment_score = {}
            for item in output[0]:
                label = item["label"]
                score = item["score"]
                sentiment_score[label] = score

            # 將情感分析結果加入到推文資料中
            tweet_info["sentiment_score"] = sentiment_score

        # 將更新後的 JSON 資料寫回原始 JSON 檔案
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
print("Finish!")
