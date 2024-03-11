import os
import json

data_folder_list = ["Data_1", "Data_2"]
for data_folder in data_folder_list:
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                weights = {"likes": 0.1, "replies": 0.3, "retweets": 0.6}
                for tweet_info in data.values():
                    weighted_sentiment_score = {}
                    weighted_sum = (
                        tweet_info["normalized_likes"] * weights["likes"]
                        + tweet_info["normalized_replies"] * weights["replies"]
                        + tweet_info["normalized_retweets"] * weights["retweets"]
                    )
                    for label, score in tweet_info["sentiment_score"].items():
                        weighted_sentiment_score[label] = (
                            tweet_info["sentiment_score"][label] * weighted_sum
                        )
                    tweet_info["weighted_sentiment_score"] = weighted_sentiment_score

                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)
