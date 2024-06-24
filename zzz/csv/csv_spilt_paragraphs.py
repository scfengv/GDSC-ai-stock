import pandas as pd
import json

input_file = "2015Q1_split_remove.csv"
output_file = "2015Q1_split_remove_paragraphs.csv"


def split_text_averagely(text, max_words):
    chunks = []
    words = text.split()  # Split the text into words
    while len(words) > max_words:
        # Find the position where the maximum word limit will be exceeded
        index = max_words
        while index < len(words) and not words[index].endswith('.'):
            index -= 1

        # If a period is found, split at that position
        if index < len(words):
            chunk = ' '.join(words[:index + 1])
            chunks.append(chunk)
            words = words[index + 1:]
    
    # Handle the remaining text
    if words:
        chunks.append(' '.join(words))
    return chunks

# Read data from CSV
data = pd.read_csv(input_file)

max_words_per_chunk = 400
output_data = []

for index, row in data.iterrows():
    paragraph = row['paragraph']  # Assuming the column name in your CSV is 'paragraph'
    if len(paragraph.split()) > max_words_per_chunk:
        chunks = split_text_averagely(paragraph, max_words_per_chunk)
        for idx, chunk in enumerate(chunks):
            output_data.append({"paragraph": chunk})
    else:
        output_data.append({"paragraph": paragraph})

# Write processed data to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv(output_file, index=False, encoding='utf-8')

print("finish", output_file)
