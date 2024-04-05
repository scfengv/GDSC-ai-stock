from transformers import pipeline
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
 
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

output_filename = '2020Q4_split_paragraphs_summarize.json'
processed_data = []

with open('2020Q4_split_paragraphs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    for key, value in item.items():
        if key.startswith('paragraph'):
            article = value
            tokenized_text = tokenizer(article, return_tensors="pt")
            outputs = model.generate(tokenized_text['input_ids'])
            
            l = len(outputs[0])
            min_new_l = int(l*2)
            max_new_l = int(l*2.5)
            print(l, min_new_l, max_new_l)
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(result)
            summary = summarizer(article, min_length=min_new_l, max_length=max_new_l, truncation=True)
            print(summary)

            processed_data.append({
                "original_text": article,
                "summary": summary[0]['summary_text']
            })

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)

print("finish!", output_filename)


'''
with open('2018Q1_split_paragraphs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    for key, value in item.items():
        if key.startswith('paragraph'):
            article = value
            tokenized_text = tokenizer(article, return_tensors="pt")

            #counter += 1
            try:
                outputs = model.generate(tokenized_text['input_ids'])
                print(outputs)
            except IndexError as e:
                print(f"Error occurred at paragraph {counter}: {e}")
                #print("Paragraph content:", article)

#text = "Our next question comes from Andrea James with Dougherty and Company.\nAndrea Susan JamesTESLA, INC. FQ1 2015 EARNINGS CALL  MAY 06, 2015\nDougherty & Company LLC, Research Division\nJust to build on the Tesla Energy conversation, what are your revenue and gross margin targets on that\nbusiness? And how do we look at the 2015 ramp?\nElon R. Musk\nCo-Founder, Chairman, Chief Executive Officer and Product Architect\nWell, I mean, the gross margin revenue obviously is going to change with time. So when it's low volume\nmade in Fremont, it will be relatively low margin. Once we get to Gigafactory up and running and -- high\nvolume and get the economies of scale working, this is just a guess right now, but I mean like maybe it's\nsomewhere around 20%. "
tokenized_text = tokenizer(text, return_tensors="pt")
outputs = model.generate(tokenized_text['input_ids'])
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
l = len(outputs[0])
min_new_l = int(l*1.5)
max_new_l = int(l*1.8)
print(l, min_new_l, max_new_l)
print(result)

summary = summarizer(text, min_length=min_new_l, max_length=max_new_l, truncation=True)
print(summary)
'''