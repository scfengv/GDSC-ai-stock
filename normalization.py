import os
import json

data_folder_list = ["Data_1", "Data_2"]
for data_folder in data_folder_list:
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
            max_likes = max(entry["likes"] for entry in data.values())
            min_likes = min(entry["likes"] for entry in data.values())
            max_replies = max(entry["replies"] for entry in data.values())
            min_replies = min(entry["replies"] for entry in data.values())
            max_retweets = max(entry["retweets"] for entry in data.values())
            min_retweets = min(entry["retweets"] for entry in data.values())

        for tweet_id, tweet_info in data.items():
            tweet_info["normalized_likes"] = (tweet_info["likes"] - min_likes) / (
                max_likes - min_likes
            )
            tweet_info["normalized_replies"] = (tweet_info["replies"] - min_replies) / (
                max_replies - min_replies
            )
            tweet_info["normalized_retweets"] = (
                tweet_info["retweets"] - min_retweets
            ) / (max_retweets - min_retweets)

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

print("Finish!!!")
