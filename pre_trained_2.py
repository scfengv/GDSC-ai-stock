import json
import os
import requests
from tqdm import tqdm

API_URL = "https://api-inference.huggingface.co/models/austinmw/distilbert-base-uncased-finetuned-tweets-sentiment"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


data_folder = "Data_2"
for filename in tqdm(os.listdir(data_folder), desc="Total file"):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        with open(file_path, "r") as file:
            data = json.load(file)

        for tweet_id, tweet_info in tqdm(data.items(), desc="Current file processing"):
            tweet_text = tweet_info["text"]
            output = query({"inputs": tweet_text})
            # 創建情感分析結果的字典(後續加入原JSON檔)
            sentiment_score = {}
            for item in output[0]:
                label = item["label"]
                score = item["score"]
                sentiment_score[label] = score

            tweet_info["sentiment_score"] = sentiment_score

        # 更新JSON檔案
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

# 改標籤名稱
for filename in tqdm(os.listdir(data_folder), desc="Total file"):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
        for tweet_id, tweet_info in data.items():
            if "LABEL_1" in tweet_info["sentiment_score"]:
                tweet_info["sentiment_score"]["neutral"] = tweet_info[
                    "sentiment_score"
                ].pop("LABEL_1")
            if "LABEL_2" in tweet_info["sentiment_score"]:
                tweet_info["sentiment_score"]["positive"] = tweet_info[
                    "sentiment_score"
                ].pop("LABEL_2")
            if "LABEL_0" in tweet_info["sentiment_score"]:
                tweet_info["sentiment_score"]["negative"] = tweet_info[
                    "sentiment_score"
                ].pop("LABEL_0")

print("Finish!")
