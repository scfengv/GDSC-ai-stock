import csv

def count_sentiments(csv_file, col_name):
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentiment = row[col_name].strip().lower()
            if sentiment == 'positive':
                positive_count += 1
            elif sentiment == 'neutral':
                neutral_count += 1
            elif sentiment == 'negative':
                negative_count += 1
    
    return positive_count, neutral_count, negative_count

csv_file_path = '2015Q1_remove_sentiment.csv'
col_name = 'label'

positive, neutral, negative = count_sentiments(csv_file_path, col_name)

print("Positive:", positive)
print("Neutral:", neutral)
print("Negative:", negative)