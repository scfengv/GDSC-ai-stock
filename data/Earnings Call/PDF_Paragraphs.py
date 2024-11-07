import json

input_file = "/Users/xuzhiwei/GDSC-ai-stock/Data/split/2024Q1_split.json"
output_file = "/Users/xuzhiwei/GDSC-ai-stock/Data/split_paragraphs/2024Q1_split_paragraphs.json"


def split_text_averagely(text, max_words):
    chunks = []
    words = text.split()
    while len(words) > max_words:
        index = max_words
        while index < len(words) and not words[index].endswith('.'):
            index -= 1

        if index < len(words):
            chunk = ' '.join(words[:index + 1])
            chunks.append(chunk)
            words = words[index + 1:]
        '''
        else:  # 若未找到句号，按照默认位置切割
            chunk_size = max_words // 2
            chunk1 = ' '.join(words[:chunk_size])
            chunk2 = ' '.join(words[chunk_size:])
            chunks.append(chunk1)
            words = words[chunk_size:]
        '''
    if words:
        chunks.append(' '.join(words))
    return chunks

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

max_words_per_chunk = 400
output_data = []

for item in data:
    paragraph = ""
    for key, value in item.items():
        if key.startswith("paragraph"):
            paragraph = value
            if len(paragraph.split()) > max_words_per_chunk:

                chunks = split_text_averagely(paragraph, max_words_per_chunk)
                for idx, chunk in enumerate(chunks):
                    output_data.append({"paragraph": chunk})
            else:
                output_data.append({"paragraph": paragraph})

with open(output_file, "w") as file:
    json.dump(output_data, file, indent=4)

print("finish", output_file)

