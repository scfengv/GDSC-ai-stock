import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import numpy as np
from scipy.special import softmax

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

sentiment_task = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

input_file = "merged2020_data.json"
output_file = "2020_sentiment(twitter).json"

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

output_data = []

for item in data:
    original_text = item.get("original_text", "") 
    for key, value in item.items():
        if key.startswith("summary"):
            summary_text = value

            summary_text = preprocess(summary_text)
            encoded_input = tokenizer(summary_text, return_tensors='pt')

            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)

            sentiment_dict = {}
            for label, score in zip(["negative", "neutral", "positive"], scores):
                sentiment_dict[label] = float(score)
            output_data.append({
                "original_text": original_text,
                "summary": summary_text,
                "sentiment": sentiment_dict
            })

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(output_data, file, indent=4, ensure_ascii=False)

print("finish！", output_file)
