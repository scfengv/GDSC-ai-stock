from transformers import pipeline
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
 
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

output_filename = '/Users/xuzhiwei/GDSC-ai-stock/Data/summary/2024Q1_split_paragraphs_summarize.json'
processed_data = [] 
with open('/Users/xuzhiwei/GDSC-ai-stock/Data/split_paragraphs/2024Q1_split_paragraphs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    for key, value in item.items():
        if key.startswith('paragraph'):
            article = value
            tokenized_text = tokenizer(article, return_tensors="pt")
            outputs = model.generate(tokenized_text['input_ids'])
            
            l = len(outputs[0])
            #min_new_l = int(l*2)
            #max_new_l = int(l*2.5)
            #print(l, min_new_l, max_new_l)
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(result)
            summary = summarizer(article, truncation=True)
            print(summary)

            processed_data.append({
                "original_text": article,
                "summary": summary[0]['summary_text']
            })

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)

print("finish!", output_filename)