import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import json

# Load the BART model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Input and output file paths
input_csv = '2015Q1_split_remove_paragraphs.csv'
output_csv = '2015Q1_remove_summary.csv'

# Read data from CSV
data = pd.read_csv(input_csv)

# Initialize a list to store processed data
processed_data = []

# Process each row in the CSV
for index, row in data.iterrows():
    article = row['paragraph']  # Assuming the column name in your CSV is 'paragraph'
    tokenized_text = tokenizer(article, return_tensors="pt")
    outputs = model.generate(tokenized_text['input_ids'])
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(result)
    summary = summarizer(article, truncation=True)
    print(summary)

    processed_data.append({
        "original_text": article,
        "summary": summary[0]['summary_text']
    })

# Convert processed data to DataFrame
processed_df = pd.DataFrame(processed_data)

# Write processed data to CSV
processed_df.to_csv(output_csv, index=False, encoding='utf-8')

print("finish!", output_csv)
