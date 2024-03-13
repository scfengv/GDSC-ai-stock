import numpy as np
import json
import os


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


data_folder_list = ["Data_1", "Data_2"]
for data_folder in data_folder_list:
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                for tweet_info in data.values():
                    sigmoid_sentiment_score = {}
                    for label, score in tweet_info["weighted_sentiment_score"].items():
                        sigmoid_sentiment_score[label] = sigmoid(
                            tweet_info["weighted_sentiment_score"][label]
                        )
                    tweet_info["sigmoid_sentiment_score"] = sigmoid_sentiment_score
                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)
print("Finished!!!")
