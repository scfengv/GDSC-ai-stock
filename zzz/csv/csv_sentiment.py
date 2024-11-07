import csv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import numpy as np
from scipy.special import softmax
import datetime

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

MODEL = "austinmw/distilbert-base-uncased-finetuned-tweets-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

sentiment_task = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

input_file = "2015Q1_remove_summary.csv"
output_file = "2015Q1_remove_sentiment.csv"

data = []
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

output_data = []

for item in data:
    #date_str = item.get("Date", "")
    #date_obj = datetime.datetime.strptime(date_str, "%Y/%m/%d") if date_str else None
    original_text = item.get("original_text", "") 
    summary_text = item.get("summary", "")  # 获取"summary"键的值，如果不存在则返回空字符串

    if summary_text :
    # and date_obj
        summary_text = preprocess(summary_text)
        encoded_input = tokenizer(summary_text, return_tensors='pt')
   
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        sentiment_dict = {}
        for label, score in zip(["negative", "neutral", "positive"], scores):
            sentiment_dict[label] = float(score)
        output_data.append({
            #"Date": date_obj.strftime("%Y-%m-%d"),
    
            "Original_text": original_text,
            "Summary": summary_text,
            "negative": sentiment_dict["negative"],
            "neutral": sentiment_dict["neutral"],
            "positive": sentiment_dict["positive"]
        })

with open(output_file, "w", encoding="utf-8", newline='') as file:
    fieldnames = ["Date", "Original_text", "Summary", "negative", "neutral", "positive"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in output_data:
        writer.writerow(row)

print("finish！", output_file)
